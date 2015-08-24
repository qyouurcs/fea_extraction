#!/usr/bin/python

import sys
import os


if __name__ == '__main__':

    if len(sys.argv) < 5:
        print 'Usage: {0} <nearest_mapping_fn.txt> <dst> <src> <save_dir> [num=100]'.format(sys.argv[0])
        sys.exit()

    mapping_fn = sys.argv[1]
    save_dir = sys.argv[4]
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
        
    dict_dst_imgs = {}
    dict_src_imgs = {}
    
    for root, subdirs, fns in os.walk(sys.argv[2]):
        for fn in fns:
            dict_dst_imgs[os.path.basename(fn)] = os.path.join(root, fn)
    
    for root, subdirs, fns in os.walk(sys.argv[3]):
        for fn in fns:
            dict_src_imgs[os.path.basename(fn)] = os.path.join(root, fn)
   
    dict_nearest_mapping = {}
    with open(mapping_fn,'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            dict_nearest_mapping[os.path.basename(parts[0])] = parts[1:]

    # Now we need to write the html code.
    header = '''
    <div style="width: 100%"; margin-top: 20px;">
    <table align="center" style="width: 100%">
    <tr>
        <td align="center">
           <img src="{0}"/>
        </td>
    </tr>
    <tr>
    <td>
        <table align="center" style="width: 100%" border="1">
    '''

    arow = '''<td width="25%"><img src="{0}" width="97%" height="auto" /></td>'''
    end = '''</table>
    </td>
    </tr>
    </table>'''
    total_ = 100
    idx = 0
    for src in dict_nearest_mapping:

        html_fn = os.path.splitext(os.path.basename(src))[0] + '.html' 
        html_fn = os.path.join(save_dir, html_fn)
        html_fid = open(html_fn, 'w')
        html_fid.write(header.format(dict_src_imgs[os.path.basename(src)]))
                
        row_cnt = 0
        for dst in dict_nearest_mapping[os.path.basename(src)]:
            if not row_cnt % 4:
                if row_cnt > 0:
                    html_fid.write('</tr>\n')
                html_fid.write('<tr>\n')
            html_fid.write(arow.format(dict_dst_imgs[os.path.basename(dst)]))
            row_cnt += 1
        html_fid.write(end)
        html_fid.write('</tr>\n')
        html_fid.close()
        idx += 1
        if idx > total_:
            sys.exit()

    
