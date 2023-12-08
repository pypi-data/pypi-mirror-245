# pvr2image
A Python module to easily convert Dreamcast/Naomi .PVR and .PVP files to images + palettes
Please note it requires Pillow (PIL) module installed

## Installation

```bash
pip3 install pvr2image
```

## Example

```import pvr2image

files_lst = [r"c:\temp\ALWAY.pvr",
               r"c:\temp\test\565_tw.pvr"]
out_dir = 'Extracted'
flip = ''                    
fmt = 'png'

pvr2image.decode(files_lst,fmt,out_dir,flip)```

# Image flip options:
''   = None
'v'  = vertical flip
'h'  = horizontal flip
'vh' = vertical and horizontal flip


## Credits

- Egregiousguy for YUV420 to YUV420p conversion
- Kion for VQ handling and logic
- tvspelsfreak for SR conversion info on Bump to normal map
