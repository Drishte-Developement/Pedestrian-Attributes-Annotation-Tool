from __future__ import division
from PIL import Image as PImage, ImageTk
import os
import sys
import glob
import random

if(sys.version_info[0] == 2):
    from Tkinter import *
    import tkMessageBox
elif(sys.version_info[0] == 3):
    from tkinter import *
    from tkinter import messagebox as tkMessageBox

gender=['male','female']
age=['0-12','13-17','18-24','25-34','35-44','45-54','55-60','60+']
hair_size=['long','short','bald']
hair_color=['black','white','colored','blonde','None']
body_orientation=['frontal','left','right','back']
face_orientation=['frontal','left','right','back']
glasses_color=['None','transparent','colored']
upper_cloth_color=['red','orange','yellow','green','blue','pink','black','brown','grey','white']
lower_cloth_color=['red','orange','yellow','green','blue','pink','black','brown','grey','white']
sleeve_length=['sleeve-less','half-sleeve','full-sleeve']
lower_body_cloth_length=['Above-knee','At-knee','At-ankle','Max']
upper_body_dress_type=['shirt','tshirt','coat','jacket','kurta','saree','top']
lower_body_dress_type=['short','jeans','pant','salwar','skirt','lower']
sports_wear=['YES','NO']
footwear=['None','sneakers','flip-flops','sandels','heels','boots','loafers']
footwear_color=['None','red','orange','yellow','green','blue','pink','black','brown','grey','white']
backpack=['None','red','orange','yellow','green','blue','pink','black','brown','grey','white']
handbag=['None','red','orange','yellow','green','blue','pink','black','brown','grey','white']
hat=['yes','no']
parent=['yes','no']
beard=['None','patchy','full']
beard_color=['None','black','white','colored','blonde']

# image sizes for the examples
SIZE = 256, 256

classes = ["person"]


class LabelTool():
    def __init__(self, master):
        # set up the main frame
        self.curimg_h = 0
        self.curimg_w = 0
        
        self.cur_cls_id = -1
        self.cur_age_id=-1
        self.cur_hair_size_id=-1
        self.cur_haircolor_id = -1
        self.cur_body_orientation_id=-1
        self.cur_face_orientation_id=-1
        self.cur_glasscolor_id=-1
        self.cur_upclothcolor_id=-1
        self.cur_loclothcolor_id=-1
        self.cur_loclothlen_id=-1
        self.cur_sleevelen_id=-1
        self.cur_lodresstype_id=-1
        self.cur_updresstype_id=-1
        self.cur_sportswear_id=-1
        self.cur_footwear_id=-1
        self.cur_footwearcol_id=-1
        self.cur_backpack_id=-1
        self.cur_handbag_id=-1
        self.cur_hat_id=-1
        self.cur_parent_id=-1
        self.cur_beard_id=-1
        self.cur_beardcol_id=-1
        
        self.cur_gx_id = 0
        
        self.parent = master
        self.parent.title("Annotation Tool")
        self.frame = Frame(self.parent, bg='MediumPurple1')
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width = FALSE, height = FALSE)
        #self.parent.resizable(0,0)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0


        # ----------------- GUI stuff ---------------------
        # dir entry & load
        self.label = Label(self.frame, text = "Image Dir:")
        self.label.grid(row = 0, column = 0, sticky = E)
        self.entry = Entry(self.frame)
        self.entry.focus_set()
        self.entry.bind('<Return>', self.loadEntry)
        self.entry.grid(row = 0, column = 1, sticky = W+E)
        self.ldBtn = Button(self.frame, text = "Load", command = self.loadDir)
        self.ldBtn.grid(row = 0, column = 3, sticky = W+E)
        
        
        self.tkvar = StringVar(self.parent)
        self.cur_cls_id = 0
        self.tkvar.set(classes[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvar, *classes,command = self.change_dropdown)
        self.popupMenu.grid(row = 1, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Choose Class:')
        self.chooselbl.grid(row = 1, column = 2, sticky = W+S)


        #g
        self.tkvargx = StringVar(self.parent)
        self.cur_gx_id = 0
        self.tkvargx.set(gender[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvargx, *gender,command = self.change_dropdowngx)
        self.popupMenu.grid(row = 1, column = 9, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Choose Gender:')
        self.chooselbl.grid(row = 1, column = 7, sticky = W+S)

                
        #age
        self.tkvara = StringVar(self.parent)
        self.cur_age_id = 0
        self.tkvara.set(age[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvara, *age,command = self.change_dropdown_a)
        self.popupMenu.grid(row = 2, column = 9, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Age:')
        self.chooselbl.grid(row = 2, column = 7, sticky = W+S)
        
        #hairsize
        self.tkvarhs = StringVar(self.parent)
        self.cur_hair_size_id = 0
        self.tkvarhs.set(hair_size[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarhs, *hair_size,command = self.change_dropdown_hs)
        self.popupMenu.grid(row = 3, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Hair size:')
        self.chooselbl.grid(row = 3, column = 2, sticky = W+S)
        
        #hair color
        self.tkvarhc = StringVar(self.parent)
        self.cur_hair_color_id = 0
        self.tkvarhc.set(hair_color[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarhc, *hair_color,command = self.change_dropdown_hc)
        self.popupMenu.grid(row = 3, column = 9, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Hair Color:')
        self.chooselbl.grid(row = 3, column = 7, sticky = W+S)
        
        #body_orientation
        self.tkvarbo = StringVar(self.parent)
        self.cur_body_orientation_id = 0
        self.tkvarbo.set(body_orientation[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarbo, *body_orientation,command = self.change_dropdown_bo)
        self.popupMenu.grid(row = 4, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Body Orientation:')
        self.chooselbl.grid(row = 4, column = 2, sticky = W+S)
        
        #face_orientation
        self.tkvarfo = StringVar(self.parent)
        self.cur_face_orientation_id = 0
        self.tkvarfo.set(face_orientation[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarfo, *face_orientation,command = self.change_dropdown_fo)
        self.popupMenu.grid(row = 4, column = 9, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Face Orientation:')
        self.chooselbl.grid(row = 4, column = 7, sticky = W+S)
        
        #glasses_color
        self.tkvargc = StringVar(self.parent)
        self.cur_glasscolor_id = 0
        self.tkvargc.set(glasses_color[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvargc, *glasses_color,command = self.change_dropdown_gc)
        self.popupMenu.grid(row = 5, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Glass color:')
        self.chooselbl.grid(row = 5, column = 2, sticky = W+S)
        
        #upper_body_dress_type
        self.tkvarudt = StringVar(self.parent)
        self.cur_updresstype_id = 0
        self.tkvarudt.set(upper_body_dress_type[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarudt, *upper_body_dress_type,command = self.change_dropdown_udt)
        self.popupMenu.grid(row = 6, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Upper Clothing Type:')
        self.chooselbl.grid(row = 6, column = 2, sticky = W+S)
        
        #upper_cloth_color
        self.tkvarucc = StringVar(self.parent)
        self.cur_upclothcolor_id = 0
        self.tkvarucc.set(upper_cloth_color[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarucc, *upper_cloth_color,command = self.change_dropdown_ucc)
        self.popupMenu.grid(row = 6, column = 9, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Upper Clothing Color:')
        self.chooselbl.grid(row = 6, column = 7, sticky = W+S)

        #lower_body_dress_type
        self.tkvarldt = StringVar(self.parent)
        self.cur_lodresstype_id = 0
        self.tkvarldt.set(lower_body_dress_type[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarldt, *lower_body_dress_type,command = self.change_dropdown_ldt)
        self.popupMenu.grid(row = 7, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Lower Clothing Type:')
        self.chooselbl.grid(row = 7, column = 2, sticky = W+S)
        
        #lower_cloth_color
        self.tkvarlcc = StringVar(self.parent)
        self.cur_loclothcolor_id = 0
        self.tkvarlcc.set(lower_cloth_color[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarlcc, *lower_cloth_color,command = self.change_dropdown_lcc)
        self.popupMenu.grid(row = 7, column = 9, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Lower Clothing Color:')
        self.chooselbl.grid(row = 7, column = 7, sticky = W+S)

        #lower_body_cloth_length
        self.tkvarlcl = StringVar(self.parent)
        self.cur_loclothlen_id = 0
        self.tkvarlcl.set(lower_body_cloth_length[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarlcl, *lower_body_cloth_length,command = self.change_dropdown_lcl)
        self.popupMenu.grid(row = 8, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Lower Clothing Length:')
        self.chooselbl.grid(row = 8, column = 2, sticky = W+S)


        #sleeve_length
        self.tkvarsl = StringVar(self.parent)
        self.cur_sleevelen_id = 0
        self.tkvarsl.set(sleeve_length[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarsl, *sleeve_length,command = self.change_dropdown_sl)
        self.popupMenu.grid(row = 8, column = 9, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Sleeve Length:')
        self.chooselbl.grid(row = 8, column = 7, sticky = W+S)
        
        #sports_wear
        self.tkvarsw = StringVar(self.parent)
        self.cur_sportswear_id = 1
        self.tkvarsw.set(sports_wear[1]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarsw, *sports_wear,command = self.change_dropdown_sw)
        self.popupMenu.grid(row = 9, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Sports Wear:')
        self.chooselbl.grid(row = 9, column = 2, sticky = W+S)
        
        #footwear
        self.tkvarfw = StringVar(self.parent)
        self.cur_footwear_id = 0
        self.tkvarfw.set(footwear[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarfw, *footwear,command = self.change_dropdown_fw)
        self.popupMenu.grid(row = 10, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Footwear:')
        self.chooselbl.grid(row = 10, column = 2, sticky = W+S)
        
        #footwear_color
        self.tkvarfc = StringVar(self.parent)
        self.cur_footwearcol_id = 0
        self.tkvarfc.set(footwear_color[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarfc, *footwear_color,command = self.change_dropdown_fc)
        self.popupMenu.grid(row = 10, column = 9, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Footwear color:')
        self.chooselbl.grid(row = 10, column = 7, sticky = W+S)        

        #backpack
        self.tkvarbk = StringVar(self.parent)
        self.cur_backpack_id = 0
        self.tkvarbk.set(backpack[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarbk, *backpack,command = self.change_dropdown_bk)
        self.popupMenu.grid(row = 11, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Backpack:')
        self.chooselbl.grid(row = 11, column = 2, sticky = W+S)        

        
        #handbag
        self.tkvarhb = StringVar(self.parent)
        self.cur_handbag_id = 0
        self.tkvarhb.set(handbag[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarhb, *handbag,command = self.change_dropdown_hb)
        self.popupMenu.grid(row = 11, column = 9, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Handbag:')
        self.chooselbl.grid(row = 11, column = 7, sticky = W+S)        
        
        #hat
        self.tkvarhat = StringVar(self.parent)
        self.cur_hat_id = 1
        self.tkvarhat.set(hat[1]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarhat, *hat,command = self.change_dropdown_hat)
        self.popupMenu.grid(row = 12, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Hat:')
        self.chooselbl.grid(row = 12, column = 2, sticky = W+S)        
        
        #parent
        self.tkvarpt = StringVar(self.parent)
        self.cur_parent_id = 1
        self.tkvarpt.set(parent[1]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarpt, *parent,command = self.change_dropdown_pt)
        self.popupMenu.grid(row = 13, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Parent:')
        self.chooselbl.grid(row = 13, column = 2, sticky = W+S)        
        
        
        #beard
        self.tkvarbd = StringVar(self.parent)
        self.cur_beard_id = 0
        self.tkvarbd.set(beard[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarbd, *beard,command = self.change_dropdown_bd)
        self.popupMenu.grid(row = 14, column = 3, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Beard:')
        self.chooselbl.grid(row = 14, column = 2, sticky = W+S)        
        
        #beard_color
        self.tkvarbdc = StringVar(self.parent)
        self.cur_beardcol_id = 0
        self.tkvarbdc.set(beard_color[0]) # set the default option
        self.popupMenu = OptionMenu(self.frame, self.tkvarbdc, *beard_color,command = self.change_dropdown_bdc)
        self.popupMenu.grid(row = 14, column = 9, sticky = E+S)
        #print("Here:", self.tkvar)
        self.chooselbl = Label(self.frame, text = 'Beard Color:')
        self.chooselbl.grid(row = 14, column = 7, sticky = W+S)        

        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.parent.bind("<Left>", self.prevImage) # press 'a' to go backforward
        self.parent.bind("<Right>", self.nextImage) # press 'd' to go forward
        self.mainPanel.grid(row = 1, column = 1, rowspan = 10, sticky = W+N)

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 24, column = 1, columnspan = 2, sticky = W+E)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

    def loadEntry(self,event):
        self.loadDir()

    def loadDir(self, dbg = False):
        if not dbg:
            try:
                s = self.entry.get()
                self.parent.focus()
                self.category = s
            except ValueError as ve:
                tkMessageBox.showerror("Error!", message = "The folder should be numbers")
                return
        if not os.path.isdir('./Images/%s' % self.category):
           tkMessageBox.showerror("Error!", message = "The specified dir doesn't exist!")
           return
        # get image list
        self.imageDir = os.path.join(r'./Images', '%s' %(self.category))
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpeg'))
        if len(self.imageList) == 0:
            print('No .jpeg images found in the specified dir!')
            tkMessageBox.showerror("Error!", message = "No .jpg images found in the specified dir!")
            return

        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

         # set up output dir
        if not os.path.exists('./Labels'):
            os.mkdir('./Labels')
        self.outDir = os.path.join(r'./Labels', '%s' %(self.category))
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)
        self.loadImage()
        print('%d images loaded from %s' %(self.total, s))

    def loadImage(self):
        # load image
        imagepath = self.imageList[self.cur - 1]
        self.img = PImage.open(imagepath)
        self.curimg_w, self.curimg_h = self.img.size
        aspect_h = int(self.curimg_h/300)
        if self.curimg_h>300:
            aspect_w = int(self.curimg_w/aspect_h)         
            self.img = self.img.resize((aspect_w, 300))
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = max(self.tkimg.width(), 300), height = max(self.tkimg.height(), 300))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor="nw")
        #print(self.tkimg)
        #print(self.img)

        # load labels
        # self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        self.imagename = os.path.splitext(os.path.basename(imagepath))[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                temp_data_str=f.read().replace("\n","")
            temp_data=temp_data_str.split("$")
            print(temp_data)
            
            self.cur_cls_id = classes.index(temp_data[0])
            self.tkvar.set(temp_data[0])

            self.cur_gx_id = gender.index(temp_data[-1])
            self.tkvargx.set(temp_data[-1])
            
            self.cur_age_id = age.index(temp_data[2]) 
            self.tkvara.set(temp_data[2])

            self.cur_hair_size_id = hair_size.index(temp_data[3])
            self.tkvarhs.set(temp_data[3])

            self.cur_haircolor_id = hair_color.index(temp_data[4])
            self.tkvarhc.set(temp_data[4])

            self.cur_body_orientation_id = body_orientation.index(temp_data[5])
            self.tkvarbo.set(temp_data[5])

            self.cur_face_orientation_id = face_orientation.index(temp_data[6])
            self.tkvarfo.set(temp_data[6])

            self.cur_glasscolor_id = glasses_color.index(temp_data[7])
            self.tkvargc.set(temp_data[7])

            self.cur_updresstype_id = upper_body_dress_type.index(temp_data[8])
            self.tkvarudt.set(temp_data[8])

            self.cur_upclothcolor_id = upper_cloth_color.index(temp_data[9])
            self.tkvarucc.set(temp_data[9])

            self.cur_lodresstype_id =lower_body_dress_type.index(temp_data[10])
            self.tkvarldt.set(temp_data[10])

            self.cur_loclothcolor_id = lower_cloth_color.index(temp_data[11])
            self.tkvarlcc.set(temp_data[11])

            self.cur_loclothlen_id = lower_body_cloth_length.index(temp_data[12])
            self.tkvarlcl.set(temp_data[12])

            self.cur_sleevelen_id = sleeve_length.index(temp_data[13])
            self.tkvarsl.set(temp_data[13])

            self.cur_sportswear_id = sports_wear.index(temp_data[14])
            self.tkvarsw.set(temp_data[14])

            self.cur_footwear_id = footwear.index(temp_data[15]) 
            self.tkvarfw.set(temp_data[15])

            self.cur_footwearcol_id = footwear_color.index(temp_data[16])
            self.tkvarfc.set(temp_data[16])

            self.cur_backpack_id = backpack.index(temp_data[17])
            self.tkvarbk.set(temp_data[17])

            self.cur_handbag_id = handbag.index(temp_data[18])
            self.tkvarhb.set(temp_data[18])

            self.cur_hat_id =hat.index(temp_data[19])
            self.tkvarhat.set(temp_data[19])

            self.cur_parent_id = parent.index(temp_data[20])
            self.tkvarpt.set(temp_data[20])

            self.cur_beard_id = beard.index(temp_data[21])
            self.tkvarbd.set(temp_data[21])

            self.cur_beardcol_id = beard_color.index(temp_data[22])
            self.tkvarbdc.set(temp_data[22])

        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))

                
        
    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            f.write(self.tkvar.get() + "$" + "None"+ "$"+self.tkvara.get()+"$"+self.tkvarhs.get()+"$"+self.tkvarhc.get()+"$"+self.tkvarbo.get()+"$"+self.tkvarfo.get()+"$"+self.tkvargc.get()+"$"+self.tkvarudt.get()+"$"+self.tkvarucc.get()+"$"+self.tkvarldt.get()+"$"+self.tkvarlcc.get()+"$"+self.tkvarlcl.get()+"$"+self.tkvarsl.get()+"$"+self.tkvarsw.get()+"$"+self.tkvarfw.get()+"$"+self.tkvarfc.get()+"$"+self.tkvarbk.get()+"$"+self.tkvarhb.get()+"$"+self.tkvarhat.get()+"$"+self.tkvarpt.get()+"$"+self.tkvarbd.get()+"$"+self.tkvarbdc.get()+"$"+self.tkvargx.get())
            #f.write(self.class_state + "$" + self.hair_color_state+ '\n')
        print('Image No. %d saved' %(self.cur))



    def prevImage(self, event = None):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()
        else:
            tkMessageBox.showerror("Information!", message = "This is first image")

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()
        else:
            tkMessageBox.showerror("Information!", message = "All images annotated")

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

    def change_dropdown(self,*args):
        cur_cls = self.tkvar.get()
        self.cur_cls_id = classes.index(cur_cls)

    def change_dropdowngx(self,*args):
        cur_gx = self.tkvargx.get()
        self.cur_gx_id = gender.index(cur_gx)
        
    def change_dropdown_a(self,*args):
        cur_age_id = self.tkvara.get()
        self.cur_age_id= age.index(cur_age_id)
    
    def change_dropdown_hs(self,*args):
        cur_hair_size = self.tkvarhs.get()
        self.cur_hair_size_id= hair_size.index(cur_hair_size)
        
    def change_dropdown_hc(self,*args):
        cur_haircolor_id = self.tkvarhc.get()
        self.cur_haircolor_id = hair_color.index(cur_haircolor_id)

    def change_dropdown_bo(self,*args):
        cur_body_orientation_id = self.tkvarbo.get()
        self.cur_body_orientation_id = body_orientation.index(cur_body_orientation_id)

    def change_dropdown_fo(self,*args):
        cur_face_orientation_id = self.tkvarfo.get()
        self.cur_face_orientation_id = face_orientation.index(cur_face_orientation_id)

    def change_dropdown_gc(self,*args):
        cur_glasscol_id = self.tkvargc.get()
        self.cur_glasscolor_id = body_orientation.index(cur_glasscol_id)

    def change_dropdown_udt(self,*args):
        cur_udt_id = self.tkvarudt.get()
        self.cur_updresstype_id = upper_body_dress_type.index(cur_udt_id)

    def change_dropdown_ucc(self,*args):
        cur_ucc_id = self.tkvarucc.get()
        self.cur_upclothcolor_id = upper_cloth_color.index(cur_ucc_id)
        
    def change_dropdown_ldt(self,*args):
        cur_ldt_id = self.tkvarldt.get()
        self.cur_lodresstype_id = lower_body_dress_type.index(cur_ldt_id)

    def change_dropdown_lcc(self,*args):
        cur_lcc_id = self.tkvarlcc.get()
        self.cur_loclothcolor_id = lower_cloth_color.index(cur_lcc_id)

    def change_dropdown_lcl(self,*args):
        cur_lcl_id = self.tkvarlcl.get()
        self.cur_loclothlen_id = lower_body_cloth_length.index(cur_lcl_id)

    def change_dropdown_sl(self,*args):
        cur_sl_id = self.tkvarsl.get()
        self.cur_sleevelen_id = sleeve_length.index(cur_sl_id)
    
    def change_dropdown_sw(self,*args):
        cur_sw_id = self.tkvarsw.get()
        self.cur_sportswear_id = sports_wear.index(cur_sw_id)
        
    def change_dropdown_fw(self,*args):
        cur_fw_id = self.tkvarfw.get()
        self.cur_footwear_id = footwear.index(cur_fw_id)
    
    def change_dropdown_fc(self,*args):
        cur_fc_id = self.tkvarfc.get()
        self.cur_footwearcol_id = footwear_color.index(cur_fc_id)
    
    def change_dropdown_bk(self,*args):
        cur_bk_id = self.tkvarbk.get()
        self.cur_backpack_id = backpack.index(cur_bk_id)
    
    def change_dropdown_hb(self,*args):
        cur_hb_id = self.tkvarhb.get()
        self.cur_handbag_id = handbag.index(cur_hb_id)

    def change_dropdown_hat(self,*args):
        cur_hat_id = self.tkvarhat.get()
        self.cur_hat_id = hat.index(cur_hat_id)

    def change_dropdown_pt(self,*args):
        cur_pt_id = self.tkvarpt.get()
        self.cur_parent_id = parent.index(cur_pt_id)

    def change_dropdown_bd(self,*args):
        cur_bd_id = self.tkvarbd.get()
        self.cur_beard_id = beard.index(cur_bd_id)

    def change_dropdown_bdc(self,*args):
        cur_bdc_id = self.tkvarbdc.get()
        self.cur_beardcol_id = beard_color.index(cur_bdc_id)


if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
    root.resizable(width =  True, height = True)
    root.mainloop()
