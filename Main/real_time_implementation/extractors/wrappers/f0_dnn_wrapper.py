import ctypes
import os
import numpy
from pathlib import Path

class f0_dnn_wrapper(object):
    """A Python wrapper for VDNNF0RT library"""
    def __init__(self, libExtension = '.dll'): # '.so'):
        # types
        self.c_float_p = ctypes.POINTER(ctypes.c_float)
        self.c_char_p = ctypes.POINTER(ctypes.c_char)

        # load the library
        libFolder = Path(__file__).parent.parent / "lib"
        sharedLibPath = os.path.join(os.path.expandvars(libFolder), "f0-dnn", "x64", "Release_DLL", "VoDNNF0RTLib_msvc2019" + libExtension) # "Linux", "libVoDNNF0RTLib" + libExtension)

        self.dllHandler = ctypes.cdll.LoadLibrary(sharedLibPath)

        # config VDNNF0RT_GetVersion()
        self.dllHandler.VDNNF0RT_GetVersion.restype = ctypes.c_char_p

        # config VDNNF0RT_Create()
        self.dllHandler.VDNNF0RT_Create.restype = ctypes.c_void_p

        # config VDNNF0RT_Configure()
        self.dllHandler.VDNNF0RT_Configure.restype = ctypes.c_int
        self.dllHandler.VDNNF0RT_Configure.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_char), ctypes.c_void_p]

        # config VDNNF0RT_GetTotalSamplesLatency()
        self.dllHandler.VDNNF0RT_GetTotalSamplesLatency.restype = ctypes.c_int
        self.dllHandler.VDNNF0RT_GetTotalSamplesLatency.argtypes = [ctypes.c_void_p]

        # config VDNNF0RT_GetAnalysisLatency()
        self.dllHandler.VDNNF0RT_GetAnalysisLatency.restype = ctypes.c_int
        self.dllHandler.VDNNF0RT_GetAnalysisLatency.argtypes = [ctypes.c_void_p]

        # config VDNNF0RT_DoProcess()
        self.dllHandler.VDNNF0RT_DoProcess.restype = ctypes.c_int
        self.dllHandler.VDNNF0RT_DoProcess.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_void_p]

        # config VDNNF0RT_DoProcessOffline()
        self.dllHandler.VDNNF0RT_DoProcessOffline.restype = ctypes.c_int
        self.dllHandler.VDNNF0RT_DoProcessOffline.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.POINTER(ctypes.c_float), ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_void_p]

        # config VDNNF0RT_Destroy()
        self.dllHandler.VDNNF0RT_Destroy.restype = None
        self.dllHandler.VDNNF0RT_Destroy.argtypes = [ctypes.c_void_p]

        # create the voconv object needed to operate with the library
        self.libObjPtr = ctypes.c_void_p(self.dllHandler.VDNNF0RT_Create())

    def cleanup(self):
        self.dllHandler.VDNNF0RT_Destroy(self.libObjPtr)

    def configure(self, sampleRate, hopSize, windowSize, modelPath=None):
        if modelPath == None:
            modelPath = str(Path(__file__).parent.parent / "lib/model/modelweights__epoch=990500.synl")
        ret = self.dllHandler.VDNNF0RT_Configure(
            ctypes.c_int(sampleRate), 
            ctypes.c_int(hopSize), 
            ctypes.c_int(windowSize),
            modelPath.encode('utf-8'),
            self.libObjPtr)
         
        return ret

    def totalLatency(self):
        return self.dllHandler.VDNNF0RT_GetTotalSamplesLatency(self.libObjPtr)

    def analysisLatency(self):
        return self.dllHandler.VDNNF0RT_GetAnalysisLatency(self.libObjPtr)

    def process(self, frame, pitchAsCents = False):
        frameSize = frame.size
        pitch = ctypes.c_float(0.0)
        confidence = ctypes.c_float(0.0)
        pitchAsCentsParam = ctypes.c_int(1) if pitchAsCents else ctypes.c_int(0)

        self.dllHandler.VDNNF0RT_DoProcess(
            frame.ctypes.data_as(self.c_float_p),
            frameSize,
            ctypes.byref(pitch),
            ctypes.byref(confidence),
            pitchAsCentsParam,
            self.libObjPtr)

        f0 = pitch.value
        f0_confidence = confidence.value
        return f0, f0_confidence

    def processOffline(self, audio, hopSize, pitchAsCents = False):
        audioSize = audio.size
        outputSize = int(audioSize / hopSize)
        pitch = numpy.zeros(outputSize)
        confidence = numpy.zeros(outputSize)
        pitch = pitch.astype(numpy.float32)
        confidence = confidence.astype(numpy.float32)
        pitchAsCentsParam = ctypes.c_int(1) if pitchAsCents else ctypes.c_int(0)

        self.dllHandler.VDNNF0RT_DoProcessOffline(
            audio.ctypes.data_as(self.c_float_p),
            audioSize,
            pitch.ctypes.data_as(self.c_float_p),
            confidence.ctypes.data_as(self.c_float_p),
            pitchAsCentsParam,
            self.libObjPtr)
        
        return pitch, confidence

    def version(self):
        return ctypes.c_char_p(self.dllHandler.VDNNF0RT_GetVersion())
