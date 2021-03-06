from SlideRunner.dataAccess.database import *
import os

def test_database():
    DB = Database()
    assert(DB is not None)
    assert(DB.isOpen() == False)
    
    dbname = 'sample_test_database.db'
    DB.create(dbname)

    assert(DB.isOpen() == True)
    assert(DB.getDBname() == dbname)
    
    DB.insertAnnotator('John Doe')
    DB.insertAnnotator('Jane Doe')
    pers = DB.getAllPersons()
    assert((pers[0][0]=='John Doe'))
    assert((pers[0][1]==1))
    assert((pers[1][0]=='Jane Doe'))
    assert((pers[1][1]==2))

    DB.insertClass('Cell')
    DB.insertClass('Crap')

    classes = DB.getAllClasses()
    assert((classes[0][0]=='Cell'))
    assert((classes[0][1]==1))
    assert((classes[1][0]=='Crap'))
    assert((classes[1][1]==2))

    DB.insertNewSlide('BLA.tiff','blub/BLA.tiff')
    DB.insertNewSlide('BLU.tiff','blub/BLU.tiff')
    DB.insertNewSlide('BLU.tiff','blow/BLU.tiff')

    assert(DB.findSlideWithFilename('BLA.tiff','blub/BLA.tiff')==1)
    assert(DB.findSlideWithFilename('BLA.tiff','blas/BLA.tiff')==1)

    assert(DB.findSlideWithFilename('BLU.tiff','blub/BLU.tiff')==2)
    assert(DB.findSlideWithFilename('BLU.tiff','blow/BLU.tiff')==3)

    spotannos = DB.findSpotAnnotations(leftUpper=(0,0), rightLower=(10,10), slideUID=1, blinded = False, currentAnnotator=1)
    assert(len(spotannos)==0)

    DB.insertNewSpotAnnotation(xpos_orig=5,ypos_orig=5, slideUID=1, classID=2, annotator=1, type = 1)
    DB.insertNewSpotAnnotation(xpos_orig=5,ypos_orig=15, slideUID=1, classID=2, annotator=1, type = 1)
    DB.insertNewSpotAnnotation(xpos_orig=5,ypos_orig=8, slideUID=1, classID=2, annotator=2, type = 1)
    DB.insertNewSpotAnnotation(xpos_orig=5,ypos_orig=4, slideUID=1, classID=1, annotator=2, type = 1)
    DB.insertNewSpotAnnotation(xpos_orig=5,ypos_orig=4, slideUID=2, classID=2, annotator=2, type = 1)

    spotannos = DB.findSpotAnnotations(leftUpper=(0,0), rightLower=(10,10), slideUID=1, blinded = False, currentAnnotator=1)
    assert(spotannos[0][0]==5) # x coordinate
    assert(spotannos[0][1]==5) # y coordinate
    assert(spotannos[0][2]==2) # agreed Class

    assert(len(spotannos)==3) # entry 2 is not found

    # test blinded mode
    spotannos = DB.findSpotAnnotations(leftUpper=(0,0), rightLower=(10,10), slideUID=1, blinded = True, currentAnnotator=2)
    assert(spotannos[0][0]==5) # x coordinate
    assert(spotannos[0][1]==5) # y coordinate
    assert(spotannos[0][2]==0) # agreed Class is unknown, because blinded

    spotannos = DB.findSpotAnnotations(leftUpper=(0,0), rightLower=(10,10), slideUID=1, blinded = True, currentAnnotator=255)
    assert(spotannos[0][0]==5) # x coordinate
    assert(spotannos[0][1]==5) # y coordinate
    assert(spotannos[0][2]==0) # agreed Class is unknown, because blinded


    spotannos = DB.findSpotAnnotations(leftUpper=(0,0), rightLower=(10,10), slideUID=5, blinded = True, currentAnnotator=2)
    assert(len(spotannos)==0)

    # Test Circular annotations
    DB.insertNewAreaAnnotation(x1=10,y1=10,x2=20,y2=20, slideUID=1, classID=1, annotator=1, typeId=5) # circle
    DB.insertNewAreaAnnotation(x1=15,y1=10,x2=20,y2=20, slideUID=1, classID=1, annotator=1, typeId=2) # rectangle

    areaannos = DB.findAreaAnnotations(leftUpper=(0,0), rightLower=(40,40), slideUID=1, blinded = False, currentAnnotator = 0)
    # return list is: x1,y1,x2,y2,class,annoId ID, type
    print(areaannos)
    assert(areaannos[0][0] == 10)
    assert(areaannos[0][6] == 5)
    assert(len(areaannos)==2)

    assert(areaannos[1][0] == 15)
    assert(areaannos[1][6] == 2)



    # test statistics
    (names,stats) = DB.countEntryPerClass(slideID=2)
    
    assert(names[0]=='Cell')
    assert(names[1]=='Crap')

    assert(stats[0,0]==0)
    assert(stats[0,1]==1)

    assert(stats[1,0]==3)
    assert(stats[1,1]==4)


    cleanup()
    
    pass


def cleanup():
    os.remove('sample_test_database.db')
