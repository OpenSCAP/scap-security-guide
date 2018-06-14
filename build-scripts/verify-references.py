#!/usr/bin/env python2

from __future__ import print_function

import sys
import optparse
import os.path

try:
    from xml.etree import cElementTree as ElementTree
except ImportError:
    import cElementTree as ElementTree

"""
This script can verify consistency of references (linkage) between XCCDF and
OVAL, and also search based on other criteria such as existence of policy
references in XCCDF.

Purpose:
  This script can be used to perform various checks on the XCCDF
  and OVAL that is generated by the Makefile. This script limits its focus to
  the files in the src/output directory. This script is to be
  used as a development tool to aid in the creation of concise
  and structurally correct XCCDF and OVAL.

Intent:
  Help XCCDF and OVAL developers spot potential mistakes in the
  XCCDF and OVAL content that is generated by the Makefile.

Usage:
  The script assumes that your current working directory is
  src/output so if you are currently in the transforms directory:

  cd ../output
  ../transforms/verify-references.py --all-checks ./rhel7-xccdf.xml

  You may find this informative as well:

  ./verify-references.py -h
"""

# Put shared python modules in path
sys.path.insert(0, os.path.join(
        os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
        "shared", "modules"))
import ssgcommon


xccdf_ns = ssgcommon.XCCDF11_NS
oval_ns = ssgcommon.oval_namespace
ocil_cs = ssgcommon.ocil_cs

# we use these strings to look for references within the XCCDF rules
nist_ref_href = "http://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r4.pdf"
disa_ref_href = "http://iase.disa.mil/stigs/cci/Pages/index.aspx"


def parse_options():
    usage = "usage: %prog [options] xccdf_file"
    parser = optparse.OptionParser(usage=usage, version="%prog ")
    # only some options are on by default
    parser.add_option("-p", "--profile", default=False,
                      action="store", dest="profile_name",
                      help="act on Rules from this XCCDF Profile only")
    parser.add_option("--rules-with-invalid-checks", default=False,
                      action="store_true", dest="rules_with_invalid_checks",
                      help="print XCCDF Rules that reference an invalid/nonexistent check")
    parser.add_option("--rules-without-checks", default=False,
                      action="store_true", dest="rules_without_checks",
                      help="print XCCDF Rules that do not include a check")
    parser.add_option("--rules-without-severity", default=False,
                      action="store_true", dest="rules_without_severity",
                      help="print XCCDF Rules that do not include a severity")
    parser.add_option("--rules-without-nistrefs", default=False,
                      action="store_true", dest="rules_without_nistrefs",
                      help="print XCCDF Rules which do not include any NIST 800-53 references")
    parser.add_option("--rules-without-disarefs", default=False,
                      action="store_true", dest="rules_without_disarefs",
                      help="print XCCDF Rules which do not include any DISA CCI references")
    parser.add_option("--rules-with-nistrefs-outside-profile", default=False,
                      action="store_true", dest="nistrefs_not_in_profile",
                      help="print XCCDF Rules which have a NIST reference, but are not part of the Profile specified")
    parser.add_option("--rules-with-disarefs-outside-profile", default=False,
                      action="store_true", dest="disarefs_not_in_profile",
                      help="print XCCDF Rules which have a DISA CCI reference, but are not part of the Profile specified")
    parser.add_option("--ovaldefs-unused", default=False,
                      action="store_true", dest="ovaldefs_unused",
                      help="print OVAL definitions which are not used by any XCCDF Rule")
    parser.add_option("--all-checks", default=False, action="store_true",
                      dest="all_checks",
                      help="perform all checks on the given XCCDF file")
    (options, args) = parser.parse_args()
    if len(args) < 1:
        parser.print_help()
        sys.exit(1)
    return (options, args)


def get_ovalfiles(checks):
    # Iterate over all checks, grab the OVAL files referenced within
    ovalfiles = set()
    for check in checks:
        if check.get("system") == oval_ns:
            checkcontentref = check.find("./{%s}check-content-ref" % xccdf_ns)
            checkcontentref_hrefattr = checkcontentref.get("href")
            # Include the file in the particular check system only if it's NOT
            # a remotely located file (to allow OVAL checks to reference http://
            # and https:// formatted URLs)
            if not checkcontentref_hrefattr.startswith("http://") and \
               not checkcontentref_hrefattr.startswith("https://"):
                ovalfiles.add(checkcontentref_hrefattr)
        elif check.get("system") != ocil_cs:
            print("ERROR: Non-OVAL checking system found: %s"
                  % (check.get("system")))
            sys.exit(1)
    return ovalfiles


def get_profileruleids(xccdftree, profile_name):
    ruleids = []

    while profile_name:
        profile = None
        for el in xccdftree.findall(".//{%s}Profile" % xccdf_ns):
            if el.get("id") != profile_name:
                continue
            profile = el
            break

        if profile is None:
            sys.exit("Specified XCCDF Profile %s was not found.")
        for select in profile.findall(".//{%s}select" % xccdf_ns):
            ruleids.append(select.get("idref"))
        profile_name = profile.get("extends")

    return ruleids


def main():
    (options, args) = parse_options()
    xccdffilename = args[0]

    # extract all of the rules within the xccdf
    xccdftree = ElementTree.parse(xccdffilename)
    rules = xccdftree.findall(".//{%s}Rule" % xccdf_ns)

    # if a profile was specified, get rid of any Rules that aren't in it
    if options.profile_name:
        profile_ruleids = get_profileruleids(xccdftree, options.profile_name)
        prunedrules = rules[:]
        for rule in rules:
            if rule.get("id") not in profile_ruleids:
                prunedrules.remove(rule)
        rules = prunedrules

    # step over xccdf file, and find referenced oval files
    checks = xccdftree.findall(".//{%s}check" % xccdf_ns)
    ovalfiles = get_ovalfiles(checks)

    # this script only supports the inclusion of one OVAL file
    if len(ovalfiles) > 1:
        sys.exit("Referencing more than one OVAL file is not yet " +
                 "supported by this script.")

    # find important elements within the XCCDF and the OVAL
    ovalfile = os.path.join(os.path.dirname(xccdffilename), ovalfiles.pop())
    ovaltree = ElementTree.parse(ovalfile)
    # collect all compliance checks (not inventory checks, which are
    # needed by CPE)
    ovaldefs = []
    for el in ovaltree.findall(".//{%s}definition" % oval_ns):
        if el.get("class") != "compliance":
            continue

        ovaldefs.append(el)

    ovaldef_ids = [ovaldef.get("id") for ovaldef in ovaldefs]

    oval_extenddefs = ovaltree.findall(".//{%s}extend_definition" % oval_ns)
    ovaldef_ids_extended = [oval_extenddef.get("definition_ref")
                            for oval_extenddef in oval_extenddefs]
    ovaldef_ids_extended = list(set(ovaldef_ids_extended))

    check_content_refs = xccdftree.findall(".//{%s}check-content-ref"
                                           % xccdf_ns)

    xccdf_parent_map = dict((c, p) for p in xccdftree.getiterator() for c in p)
    # now we can actually do the verification work here
    if options.rules_with_invalid_checks or options.all_checks:
        for check_content_ref in check_content_refs:

            # Skip those <check-content-ref> elements using OCIL as the checksystem
            # (since we are checking just referenced OVAL definitions)
            if xccdf_parent_map[check_content_ref].get("system") == ocil_cs:
                continue

            # Obtain the value of the 'href' attribute of particular
            # <check-content-ref> element
            check_content_ref_href_attr = check_content_ref.get("href")

            # Don't attempt to obtain refname on <check-content-ref> element
            # having its "href" attribute set either to "http://" or to
            # "https://" values (since the "name" attribute will be empty for
            # these two cases)
            if check_content_ref_href_attr.startswith("http://") or \
               check_content_ref_href_attr.startswith("https://"):
                continue

            refname = check_content_ref.get("name")
            if refname not in ovaldef_ids:
                rule = xccdf_parent_map[
                    xccdf_parent_map[check_content_ref]
                ]
                print("ERROR: Invalid OVAL definition referenced by XCCDF Rule: %s"
                      % (rule.get("id")))
                sys.exit(1)

    if options.rules_without_checks or options.all_checks:
        for rule in rules:
            check = rule.find("./{%s}check" % xccdf_ns)
            if check is None:
                print("ERROR: No reference to OVAL definition in XCCDF Rule: %s"
                      % (rule.get("id")))
                sys.exit(1)

    if options.rules_without_severity or options.all_checks:
        for rule in rules:
            if rule.get("severity") is None:
                print("ERROR: No severity assigned to XCCDF Rule: %s"
                      % (rule.get("id")))
                sys.exit(1)

    if options.rules_without_nistrefs or options.rules_without_disarefs or options.all_checks:
        for rule in rules:
            # find all references in the current rule
            refs = rule.findall(".//{%s}reference" % xccdf_ns)
            if refs is None:
                print("ERROR: No reference assigned to XCCDF Rule: %s"
                      % (rule.get("id")))
                sys.exit(1)
            else:
                # loop through the Rule's references and put their hrefs
                # in a list
                ref_href_list = [ref.get("href") for ref in refs]
                # print warning if rule does not have a NIST reference
                if (nist_ref_href not in ref_href_list) and options.rules_without_nistrefs:
                    print("ERROR: No valid NIST reference in XCCDF Rule: " +
                          rule.get("id"))
                    sys.exit(1)
                # print warning if rule does not have a DISA reference
                if (disa_ref_href not in ref_href_list) and options.rules_without_disarefs:
                    print("ERROR: No valid DISA CCI reference in XCCDF Rule: " +
                          rule.get("id"))
                    sys.exit(1)

    if options.disarefs_not_in_profile or options.nistrefs_not_in_profile:
        if options.profile_name is None:
            sys.exit("The options for finding Rules with a reference, "
                     "but which are not in a Profile, requires specifying a Profile.")
        allrules = xccdftree.findall(".//{%s}Rule" % xccdf_ns)
        for rule in allrules:
            # find all references in the current rule
            refs = rule.findall(".//{%s}reference" % xccdf_ns)
            ref_href_list = [ref.get("href") for ref in refs]
            # print warning if Rule is outside Profile and has a NIST reference
            if options.nistrefs_not_in_profile:
                if (nist_ref_href in ref_href_list) and (rule.get("id") not in profile_ruleids):
                    print("ERROR: XCCDF Rule found with NIST reference outside Profile %s: "
                          % options.profile_name + rule.get("id"))
                    sys.exit(1)
            # print warning if Rule is outside Profile and has a DISA reference
            if options.disarefs_not_in_profile:
                if (disa_ref_href in ref_href_list) and (rule.get("id") not in profile_ruleids):
                    print("ERROR: XCCDF Rule found with DISA CCI reference outside Profile %s: "
                          % options.profile_name + rule.get("id"))
                    sys.exit(1)

    if options.ovaldefs_unused or options.all_checks:
        # create a list of all of the OVAL compliance check ids that are
        # defined in the oval file
        oval_checks_list = [ovaldef.get("id") for ovaldef in ovaldefs]
        # now loop through the xccdf rules; if a rule references an oval check
        # we remove the oval check from our list
        for check_content in check_content_refs:
            # remove from the list
            if check_content.get("name") in oval_checks_list:
                oval_checks_list.remove(check_content.get("name"))
        # the list should now contain the OVAL checks that are not referenced
        # by any XCCDF rule
        oval_checks_list.sort()
        for oval_id in oval_checks_list:
            # don't print out the OVAL defs that are extended by others,
            # as they're not unused
            if oval_id not in ovaldef_ids_extended:
                print("WARNING: OVAL Check is not referenced by XCCDF: %s"
                      % (oval_id))
                # Do not treat this as error but only as a warning
                # exit_value = 1


if __name__ == "__main__":
    main()
