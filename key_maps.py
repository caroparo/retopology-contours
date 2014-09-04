'''
Patrick Moore
Modify this file to chanage you default keymap for contours

Events reported at 'CTRL+SHIFT+ALT+TYPE'
eg.   'CTRL+SHIFT+A' is a valid event but 'SHIFT+CTRL+A' is not

For a list of available key types, see
http://www.blender.org/documentation/blender_python_api_2_70a_release/bpy.types.Event.html?highlight=event.type#bpy.types.Event.type

DO NOT REMOVE ANY ITEMS from the default key_maps
If you want an item unmapped, do it as follows
def_cs_map['example_op'] = {}
'''

import bpy    

def_cs_key_map = {}
def_cs_key_map['action'] = {'LEFTMOUSE'}
def_cs_key_map['select'] = {'RIGHTMOUSE'}
def_cs_key_map['modal confirm'] = {'LEFTMOUSE', 'SPACE'}
def_cs_key_map['modal cancel'] = {'RIGHTMOSUE', 'ESC'}
def_cs_key_map['modal precise'] = 'SHIFT'
def_cs_key_map['modal constrain'] = 'ALT'
def_cs_key_map['scale'] = {'S'}
def_cs_key_map['translate'] = {'G'}
def_cs_key_map['rotate'] = {'R'}
def_cs_key_map['delete'] = {'X', 'DEL'}
def_cs_key_map['up count'] = {'CTRL+NUMPAD_PLUS','CTRL+WHEELUPMOUSE'}     
def_cs_key_map['dn count'] = {'CTRL+NUMPAD_MINUS','CTRL+WHEELDOWNMOUSE'}
def_cs_key_map['bridge'] = {'B'}
def_cs_key_map['new'] = {'N'}
def_cs_key_map['align'] = {'SHIFT+A', 'CRTL+A', 'ALT+A'}
def_cs_key_map['up shift'] = {'LEFT_ARROW'}
def_cs_key_map['dn shift'] = {'RIGHT_ARROW'}
def_cs_key_map['smooth'] = {'CTRL+S'}
def_cs_key_map['view cursor'] = {'C'}
def_cs_key_map['undo'] = {'CTRL+Z'}
def_cs_key_map['mode'] = {'TAB'}
def_cs_key_map['snap cursor'] = {'SHIFT+S'}
def_cs_key_map['navigate'] = get_nav_keys(bpy.context.window_manager.key_configs['Blender'])

navigation_events = {'Rotate View', 'Move View', 'Zoom View', 
                     'View Pan', 'View Orbit', 'Rotate View', 
                     'View Persp/Ortho', 'View Numpad', 'NDOF Orbit View', 
                     'NDOF Pan View', 'View Selected', 'Center View to Cursor'}


def kmi_details(kmi):
        kmi_ctrl    = 'CTRL+'  if kmi.ctrl  else ''
        kmi_shift   = 'SHIFT+' if kmi.shift else ''
        kmi_alt     = 'ALT+'   if kmi.alt   else ''
        kmi_ftype   = kmi_ctrl + kmi_shift + kmi_alt + kmi.type
        
        return kmi_ftype
    
def get_nav_keys(keycon):
    nav_keys = set()
    if '3d View' not in keycon.keymaps:
        print('Your 3D view has no keymap, please email and post on forum')
        return nav_keys
    
    #navigation keys last, to avoid conflicts eg, Ctl + Wheel
    #center view on cursor is included in nav
    for kmi in keycon.keymaps['3D View'].keymap_items:
        if kmi.name in navigation_events:    
            nav_keys.add(kmi_details(kmi))
                
    #bug, WHEELOUTMOUSE and WHEELINMOUSE used in 3dview keymaap
    nav_keys.add('WHEELDOWNMOUSE')
    nav_keys.add('WHEELUPMOUSE')
    
    return nav_keys
    
def find_kmi_by_idname(idname, keymap = None):
    C = bpy.context
    wm = C.window_manager
    keycon = wm.keyconfigs.active
    
    kmis = []
    
    if keymap:
        keymaps = [keycon.keymaps[keymap]]
    else:
        keymaps = keycon.keymaps
    for km in keymaps:
        for kmi in km.keymap_items:
            if kmi.idname == idname:
                kmis.append(kmi_details(kmi))
                
    return kmis

    
def add_to_dict(km_dict, key,value, safety = True):   
    if safety:
        for k in km_dict.keys():
            if value in km_dict[k]:
                print('already part of keymap dictionary %s  %s' % (key, value))
                if key not in km_dict:
                    km_dict[key] = {}
                return False
            
    if key in km_dict:
        val = km_dict[key]
        
        if value not in val:
            val.add(value)
            return True
        else:
            return False
    else:
        km_dict[key] = set([value])
        return True
       
def contours_default_keymap_generate():
    km_dict = def_cs_key_map.copy()
    
    #bug, WHEELOUTMOUSE and WHEELINMOUSE used in 3dview keymap
    add_to_dict(km_dict,'navigate', 'WHEELUPMOUSE')
    add_to_dict(km_dict,'navigate', 'WHEELDOWNMOUSE')
    
    for kmi in keycon.keymaps['3D View'].keymap_items:
        if kmi.name in navigation_events:     
            add_to_dict(km_dict,'navigate',kmi_details(kmi))
            
    return km_dict
          
          
def contours_keymap():
    km_dict = {}
    C = bpy.context
    wm = C.window_manager
    keycon = wm.keyconfigs.active
    
    if '3D View' not in keycon.keymaps:
        print('you have no 3D View config in your keympa, reverting to default Blender')
        keycon = wm.keyconfigs['Blender']
    #get a backup, default keymap (which can be edited by user for overrides)
    if 'maya' in keycon.name:
        def_map = def_cs_key_map
    if '3ds' in keycon.name:
        def_map = def_cs_key_map
    else:
        def_map = def_cs_key_map
        
    #Attempt to gather user preferred actions from Blender prefs    
    sel = C.user_preferences.inputs.select_mouse
    sel += 'MOUSE'
    
    act = def_cs_key_map['action']
    nav_keys = get_nav_keys(keycon)
    
    ######################################
    #######  Selection and Action ########
    if act & nav_keys:
        print(act + ' detected in navigations keys')
        print('Please modify key_maps.py in addon directory')
        
        print('default keymap also conflicts with user navigation keys')
        bpy.ops.url_open(url = "http://cgcookiemarkets.com/blender/forums/topic/custom-modal-hotkeys/")
    else:
        print('uneventfully added action keymap :' + act)
        for key in act:
            for val in act[key]:
                add_to_dict(km_dict,'action', val, safety = False)
                add_to_dict(km_dict,'modal confirm', val, safety = False)
    if sel in nav_keys:
        print(sel + ' detected in navigations keys')
        print('This should be your selection key')
        #try default map
        if def_map['select'] not in nav_keys:
            sel = def_map['select']
            print('I see that you have handled it in your defaults, good work')
            add_to_dict(km_dict,'select', sel, safety = False)
            add_to_dict(km_dict,'modal cancel', sel, safety = True)
        else:
            print('default selection keymap also conflicts with user navigation keys')
            bpy.ops.url_open(url = "http://cgcookiemarkets.com/blender/forums/topic/custom-modal-hotkeys/")
 
    else:
        print('uneventfully added select keymap :' + act)
        add_to_dict(km_dict,'select', sel, safety = False)
        add_to_dict(km_dict, 'modal cancel', sel, safety = True) #safety so that if select and action are same

    ######################################
    ######  Grab, Rotate and Scale  ######
    trans = set(find_kmi_by_idname('transform.transate', keymap = '3D View'))
    if not trans:
        km_dict['translate'] = def_map['translate']
    else:
        km_dict['translate'] = trans
            
    rot = set(find_kmi_by_idname('transform.rotate', keymap = '3D View'))
    if not rot:
        km_dict['rotate'] = def_map['rotate']
    else:
        km_dict['rotate'] = rot 
    
    scale = set(find_kmi_by_idname('transform.resize', keymap = '3D View'))
    if not scale:
        km_dict['scale'] = def_map['scale']
    else:
        km_dict['scale'] = scale
        
    ##################################
    ######  Regular Operators  ####### 
    for key in ['up count', 'dn count', 'bridge','new','align','up shift','dn shift','smooth', 'snap cursor','view cursor','undo','mode', 'delete']:
        for val in def_map[key]:
            if not add_to_dict(km_dict, key, val, safety = True):
                print('left out %s key for %s operator' % (val, key))
                print('check your defaults')

    #navigation keys last, to avoid conflicts eg, Ctl + Wheel
    #center view on cursor is included in nav
    for kmi in keycon.keymaps['3D View'].keymap_items:
        if kmi.name in navigation_events:
                
            if not add_to_dict(km_dict,'navigate', kmi_details(kmi)):
                print('Left out %s navigation, collision with other key' % kmi.name)
                
    #bug, WHEELOUTMOUSE and WHEELINMOUSE used in 3dview keymaap
    add_to_dict(km_dict,'navigate', 'WHEELDOWNMOUSE')
    add_to_dict(km_dict,'navigate', 'WHEELUPMOUSE')
    
    return km_dict