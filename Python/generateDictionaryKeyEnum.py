#!/usr/bin/env python

'''
    Copyright (C) 2014 Parrot SA

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the 
      distribution.
    * Neither the name of Parrot nor the names
      of its contributors may be used to endorse or promote products
      derived from this software without specific prior written
      permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
    OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED 
    AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
    OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.
'''

import sys
import os
import re

MYDIR=os.path.abspath(os.path.dirname(sys.argv[0]))
if '' == MYDIR:
    MYDIR=os.getcwd()

sys.path.append('%(MYDIR)s/../../ARBuildUtils/Utils/Python' % locals())

DEVICE_CONTROLLER_FILE_NAME = 'deviceControllers.xml'
DEVICE_CONTROLLER_FILE = MYDIR+'/../Xml/'+DEVICE_CONTROLLER_FILE_NAME

from ARFuncs import *
from ARCommandsParser import *
from ARControllerUtils import *

def generateDictionaryKeyEnum (allFeatures, SRC_DIR, INC_DIR):
    
    deviceControllers = parseDeviceControllersXml (DEVICE_CONTROLLER_FILE, allFeatures)
    
    #check deviceController list
    if not deviceControllers:
        exit (1)
        
    for d in deviceControllers:
        ARPrint ('    name: ' + d.name)
    
    ARPrint ('generateDictionaryKeyEnum ...')
    
    #########################################
    # Write Feature controller header file  #
    #########################################

    includeDefine = '_' + MODULE_DICTIONARY + '_KEY_H_'

    headerFileName = 'ARCONTROLLER_DICTIONARY_Key.h'
    bref = '.h'
    filepath = INC_DIR + headerFileName
    hFile = open (filepath, 'w')

    hFile.write ('/**********************************************************\n')
    hFile.write (' *            AUTOGENERATED FILE                          *\n')
    hFile.write (' *             DO NOT MODIFY IT                           *\n')
    hFile.write (' *                                                        *\n')
    hFile.write (' * To add new commands :                                  *\n')
    hFile.write (' *  - Modify ../Xml/commands.xml file                     *\n')
    hFile.write (' *  - Re-run generateDictionaryKeyEnum.py script          *\n')
    hFile.write (' *                                                        *\n')
    hFile.write (' **********************************************************/\n')
    hFile.write ('\n')

    hFile.write ('/**\n')
    hFile.write ('* @file '+headerFileName+'\n')
    hFile.write ('* @brief '+bref+'\n')
    hFile.write ('*/\n')
    hFile.write ('\n')

    hFile.write ('#ifndef '+includeDefine+'\n')
    hFile.write ('#define '+includeDefine+'\n')
    hFile.write ('\n')
    
    hFile.write ('/**\n')
    hFile.write (' * \n') # TODO add !!!!!!!!!!!!!!!!!!!!!!!!!!
    hFile.write (' */\n')
    hFile.write ('typedef enum \n')
    hFile.write ('{\n')
    first = True
    for feature in allFeatures:
        if first:
            hFile.write ('    '+defineNotification(feature)+' = 0, /**< Key used to define the feature <code>' + ARCapitalize (feature.name) + '</code> */\n')
            first = False
        else:
            hFile.write ('    '+defineNotification(feature)+', /**< Key used to define the feature <code>' + ARCapitalize (feature.name) + '</code> */\n')
        
        for cl in feature.classes:
            
            if isEvent(cl) or isState(cl):
                for cmd in cl.cmds:
                    hFile.write ('    '+defineNotification(feature, cl, cmd)+', /**< Key used to define the command <code>' + ARCapitalize (cmd.name) + '</code> of class <code>' + ARCapitalize (cl.name) + '</code> in project <code>' + ARCapitalize (feature.name) + '</code> */\n')
    hFile.write ('    '+AREnumValue(MODULE_DICTIONARY, 'DICTIONARY', 'KEY','MAX')+', /**< Unused, iterator maximum value */\n')
    hFile.write ('}'+defineNotificationDef()+';\n')
    hFile.write ('\n')
    
    # TODO add !!!!!!!!!!!!!!!!!!!!!!!!!!
    hFile.write (''+defineNotificationDef()+' ' + ARFunctionName (MODULE_DICTIONARY, 'Key', 'GetFeatureFromCommandKey')+' ('+defineNotificationDef()+' commandKey);\n')
    
    hFile.write ('#endif /* '+includeDefine+' */\n')
    hFile.write ('\n')
    hFile.write ('// END GENERATED CODE\n')
    hFile.close ()
    
    #################################################
    # Write Feature controller c file               #
    #################################################
    
    classTag = 'ARCONTROLLER_Device'
    
    cFileName = 'ARCONTROLLER_DICTIONARY_Key.c'
    filepath = SRC_DIR + cFileName
    cFile = open (filepath, 'w')

    cFile.write ('/**********************************************************\n')
    cFile.write (' *            AUTOGENERATED FILE                          *\n')
    cFile.write (' *             DO NOT MODIFY IT                           *\n')
    cFile.write (' *                                                        *\n')
    cFile.write (' * To add new commands :                                  *\n')
    cFile.write (' *  - Modify ../Xml/commands.xml file                     *\n')
    cFile.write (' *  - Re-run generateDictionaryKeyEnum.py script          *\n')
    cFile.write (' *                                                        *\n')
    cFile.write (' **********************************************************/\n')
    cFile.write ('\n')

    cFile.write ('/**\n')
    cFile.write ('* @file '+cFileName+'\n')
    cFile.write ('* @brief '+bref+'\n')
    cFile.write ('*/\n')
    cFile.write ('\n')

    cFile.write ('#include <stdio.h>\n')
    cFile.write ('\n')
    
    cFile.write ('#include <libARController/ARCONTROLLER_DICTIONARY_Key.h>\n')
    cFile.write ('\n')
    
    cFile.write (''+defineNotificationDef()+' ' + ARFunctionName (MODULE_DICTIONARY, 'Key', 'GetFeatureFromCommandKey')+' ('+defineNotificationDef()+' commandKey)\n')
    cFile.write ('{\n')
    cFile.write ('    // -- Get Feature From Command Key --\n')
    cFile.write ('    \n')
    
    cFile.write ('    '+defineNotificationDef()+' featrueKey = '+AREnumValue(MODULE_DICTIONARY, 'DICTIONARY', 'KEY','MAX')+';\n')
    cFile.write ('    \n')
    
    cFile.write ('    // find feature parameters\n')
    first = True
    for index in range(len(allFeatures)-1):
    
        feature = allFeatures[index]
        featureNext = allFeatures[index+1]
        
        ifOrElse = 'if'
        if first:
            ifOrElse = 'if'
            first = False
        else:
            ifOrElse = 'else if'
        
        nextKey = ''
        if index != (len(allFeatures)-1):
            nextKey = defineNotification(featureNext)
        else:
            nextKey = AREnumValue(MODULE_DICTIONARY, 'DICTIONARY', 'KEY','MAX')
        
        cFile.write ('    '+ifOrElse+' ('+defineNotification(feature)+' <= commandKey && commandKey < '+nextKey+')\n')
        cFile.write ('    {\n')
        cFile.write ('        featrueKey = '+defineNotification(feature)+';\n')
        cFile.write ('    }\n')
    cFile.write ('    \n')
        
    cFile.write ('    return featrueKey;\n')
    cFile.write ('}\n')
    cFile.write ('\n')
    
    cFile.close ()
