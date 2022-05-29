import fitz

def Main():
    getPDF()

def getPDF():
    path_to_PDF = input('Which PDF are we dealing with today? Please specify the direct file path:\n')

    try:
        file_name = path_to_PDF.split('/')[-1]
        outFile = file_name
        f = fitz.open(path_to_PDF)
        maxPages = f.pageCount
    except:
        print('An error occurred. Please try again.')
        getPDF()
    
    getPagesToDelete(maxPages,outFile,f,getPDF)


def validator(pages,maxPages,getPagesToDelete,outFile):
    try:
        preProcess_pagesToDelete = [ int(x) for x in pages.split(' ') ]

        validation = all((x > 0 and x < maxPages) for x in preProcess_pagesToDelete)

        if(not validation):
            print('You have entered an invalid page number. Please try again.\n')
            getPagesToDelete(maxPages,outFile)

    except:
        print('You have not entered valid numbers. Please try again.')
        getPagesToDelete(maxPages,outFile)

    return preProcess_pagesToDelete

    #Got it!
    #That's not a PDF! Try again?
def getPagesToDelete(maxPages,outFile,f,getPDF):
    print('Which pages would you like to delete?:\n' )
    print('Please enter the page numbers separated with a <space>:\n')
    pages = input( f'Max number of pages is { maxPages }:\n')

    # Check types and bounds
    preProcess_pagesToDelete = validator(pages,maxPages,getPagesToDelete,outFile)

    try:
        total_pages = [ x for x in range(maxPages) ]
        
        pagesToDelete = [ *map(lambda x: x - 1, preProcess_pagesToDelete) ]
    except:
        print('Something went wrong. Please try again.\n')
        getPagesToDelete(maxPages,outFile)

    remaining_pages = getRemainingPages(total_pages,pagesToDelete)

    confirmPagesAndWriteFile(pages,outFile,f,getPagesToDelete,maxPages,remaining_pages,getPDF)

    
def getRemainingPages(total_pages, pagesToDelete):
    remaining_pages = list(set(total_pages) - set(pagesToDelete))
    return remaining_pages

def checkValidYesOrNo(instr):
    isValid = (instr == 'y' or instr == 'n')
    return isValid

def editAnother(getPDF):
    another = input('Your new PDF has been saved. Would you like to edit another? (y|n):\n')
    val = checkValidYesOrNo(another)
    if(val):
        if(another == 'y'):
            print('Great! Starting over...\n')
            getPDF()
        if(another == 'n'):
            print('See you again soon.\n')
    else:
        print('Invalid selection. Please try again.\n')
        editAnother()
    

def confirmPagesAndWriteFile(pages,outFile,f,getPagesToDelete,maxPages,remaining_pages,getPDF):
    correctPagesForDeletion = input(f'Confirm you\'d like to remove pages {pages} from your document? (y|n):\n')
    isVal = checkValidYesOrNo(correctPagesForDeletion)
    if(isVal):
        if(correctPagesForDeletion == 'y'):
            newFile = input(f'All set! Would you like to write the changes to a new file? (y|n):\n')
            isVal2 = checkValidYesOrNo(newFile)
            if(isVal2):
                if(newFile == 'y'):
                    outFile = input('Please enter the name of the new file:\n')
                
                print(f'Writing changes to file: {outFile}.pdf')
                f.select(remaining_pages)
                f.save(outFile + '.pdf')
                editAnother(getPDF)


        elif(correctPagesForDeletion == 'n'):
            # Select new pages -> User doesn't want to remove these
            print('Please reselect your pages:\n')
            getPagesToDelete(maxPages,outFile,f,getPDF)
    else:
        print('Invalid selection. Please try again:\n')
        confirmPagesAndWriteFile(pages,outFile,f,getPagesToDelete,maxPages)
              
Main()