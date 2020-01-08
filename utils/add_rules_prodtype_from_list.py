#!/usr/bin/env python3
 
import sys
import os
import argparse
import json
 
import ssg.rules
import ssg.utils
import ssg.rule_yaml
 
import mod_prodtype
 
SSG_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

#script en sucio de prueba
#Este script añade el producto deseado(ej. sle) al campo de productos afectados de cada regla de una lista de reglas dada
#Ejemplo de uso(quitar comillas): utils/add_rules_prodtype_from_list.py '/ruta_archivo_reglas' 'add' 'sle11'
 
def main():
 
    if len(sys.argv) > 4:
        print("Demasiados argumentos")
    else:
        file = open(sys.argv[1], 'r')
        action = sys.argv[2]
        ruleArray = file.readlines()
        ruleArray = [x.strip() for x in ruleArray]
        file.close()
 
        if action=="list" or (action=="add" and len(sys.argv) > 2):
            for rule in ruleArray:
                if action=="list":
                    os.system('~/content/utils/mod_prodtype.py {} {}'.format(rule, action))
                elif action=="add":
                    product = sys.argv[3]
                    os.system('~/content/utils/mod_prodtype.py {} {} {}'.format(rule, action, product))
        else:
            print("Especifique la opcion correcta deseada(list or add)")
 
 
if __name__ == "__main__":
    main()

