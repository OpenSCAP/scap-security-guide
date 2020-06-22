# platform = Java Runtime Environment
JAVA_PROPERTIES="/etc/.java/deployment/deployment.properties"

grep -q "^deployment.security.blacklist.check=true$" ${JAVA_PROPERTIES} && \
sed -i "s/deployment.security.blacklist.check=.*/deployment.security.blacklist.check=true/g" ${JAVA_PROPERTIES}
if ! [ $? -eq 0 ] ; then
  echo "deployment.security.blacklist.check=true" >> ${JAVA_PROPERTIES}
fi

grep -q "^deployment.security.blacklist.check.locked$" ${JAVA_PROPERTIES} && \
sed -i "s/deployment.security.blacklist.check\..*/deployment.security.blacklist.check.locked/g" ${JAVA_PROPERTIES}
if ! [ $? -eq 0 ] ; then
  echo "deployment.security.blacklist.check.locked" >> ${JAVA_PROPERTIES}
fi
