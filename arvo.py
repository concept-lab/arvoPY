import glob 
import sys
import os
import numpy as np
# check if .so present, if more  than one ask user
libfile = [n for n in glob.glob('*.so') ]

if len(libfile) ==1 :
    libname = libfile[0]
    libname = os.path.abspath(libname)
    print(libname)
elif len(libfile) == 0:
    try:
        raise Exception
    except Exception:
        print("Exception: No C shared library in the working directory")
        sys.exit()
elif len(libfile) >1:
    try:
        raise Exception("Multiple C shared library in the working directory!")
    except Exception:
        raise



 #INITIALIZATION OF C FUNCTIONS


import ctypes

Cfunc = ctypes.CDLL(libname)

volumeArvo_C=Cfunc.ARVOLUME_C
volumeArvo_C.argtypes=[ctypes.POINTER(ctypes.c_void_p),ctypes.POINTER(ctypes.c_void_p),ctypes.c_int]
volumeArvo_C.restype = None #error message: 0 success , -1 fail

simpleV_C=Cfunc.simpleV
simpleV_C.argtypes=[ctypes.POINTER(ctypes.c_void_p),ctypes.c_int]
simpleV_C.restype=ctypes.c_double


def arvoVol(coordinates):
    from time import time
    
    '''
    Volume calculator wrapper to invoke C written ARVO module
    INPUT: Matrix containing spheres coordinates and radius.
    Must be first transformed in a contiguous Ctype array.
    Every 4-blocks of memory store x,y,z, and r for a given probe sphere
    '''
    
    coordinates = np.array(coordinates) #Now is a nx4 matrix
    n = coordinates.shape[0]
    # print("\n Number of probes",n)
    start = time()
    # print(coordinates)
    #C wrappers ##
    coordinates = np.ascontiguousarray(coordinates,dtype = ctypes.c_double)
    pcoord = coordinates.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p))
    n = ctypes.c_int(n)
    # print("n=",n,ctypes.sizeof(n))

    result = np.empty(2)
    result = np.ascontiguousarray(result,dtype = ctypes.c_double)
    pres = result.ctypes.data_as(ctypes.POINTER(ctypes.c_void_p))
    ##

    volumeArvo_C(pres,pcoord,n)
    # print(err)
    # if(err==-1):
    #     exit("Error occurred during volume computation") 

    volume = result[0]
    area = result[1]  #Ready if needed..

    end = time()
    Localtime_elapsed=end - start
    print("Elapsed time = ", Localtime_elapsed)
    return volume,area

############################################ 
##########

def readCoord(fp):
    coord =[]
    for l in fp.readlines():
        print(l)
        coord.append([float(c) for c in l.split()])
    return np.array(coord)
def main(argv):
    
    import getopt

    try:
        opts, args = getopt.getopt(argv,"h",["help"])
    except getopt.GetoptError:
        print ('uncorrect formatting of options')
        sys.exit(2)
    for opt, arg in opts:
        if opt in["-h","--help"]:
            print("Usage: python3 arvo.py <spheres_coordinates.xyzr>")
    # Read coordinates from xyzr matrix 
    try:
        name = args[0]
    except Exception:
        print("No input file given.\n For help type python3 arvo.py -h")
        sys.exit(2)


    print(name)
    try:
        inputFile = open(name,'r')
    except Exception as error:
        print('An exception occurred while reading file: {}'.format(error))
    
    coords = readCoord(inputFile)
    print(coords)

    vol,area = arvoVol(coords)

    print("vol = %.5f\t area = %.5f"%(vol,area))



if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("\nUser exit")
        sys.exit()