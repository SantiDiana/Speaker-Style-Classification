/*--------------------------------------------------------------------------------
 file VoDNNF0RTLib_api.h
 version 1.1 [21092021]

 Copyright (C) 2011-2021 Voctro Labs S.L.,
 All rights reserved

 CONFIDENTIAL: This document contains confidential information.
 Do not disclose any information contained in this document to any
 third-party without the prior written consent of Voctro Labs S.L.
 --------------------------------------------------------------------------------*/

// This file contains all the prototypes needed for using
// the VoDNNF0RT Library


#ifndef __VODNNF0RTLIB__
#define __VODNNF0RTLIB__

#ifndef __APPLE__
  #ifdef VDNNF0RT_AS_DLL
    #define VDNNF0RT_DLLEXPORT __declspec(dllexport)
  #else
    #define VDNNF0RT_DLLEXPORT
  #endif
#else
  #define VDNNF0RT_DLLEXPORT __attribute__((visibility("default")))
#endif

#include "stdint.h"

#ifdef __cplusplus
extern "C" {
#endif //__cplusplus

  ///////////////////////////////////////////
  ///// CREATE / DESTROY
  ///////////////////////////////////////////

  /**
   Create VDNNF0RT Object, the returned object will be passed as parameter to all API functions

   @return : pointer to VDNNF0RT object instance
  */
  VDNNF0RT_DLLEXPORT void* VDNNF0RT_Create();

  /**
   Destroy VDNNF0RT Object, to be called when finished using the library to release all memory

   @param VF0RT : pointer to VDNNF0RT object instance, created in VDNNF0RT_Create()
  */
  VDNNF0RT_DLLEXPORT void VDNNF0RT_Destroy(void* VDNNF0RT);

  ///////////////////////////////////////////
  ///// CONFIGURE
  ///////////////////////////////////////////

  /**
   Call this function to configure init parameters of the VoF0RTLib Library
   @param sampleRate : samplingrate in Hz of the input audio (supports 11025, 16000, 22050, 
                       24000, 32000, 44100 & 48000)
   @param hopSize : number of samples of hopsize from previous analysis frame
   @param windowSize : number of samples for each window to be processed
   @param modelFn : char pointer containing the name of the dnnf0 model file, to use the default 
                    model you can set it to en empty string ""
   @param VDNNF0RT : pointer to VDNNF0RT object instance, created in VDNNF0RT_Create()

   @return : 0 if ok, < 0 if error
  */
  VDNNF0RT_DLLEXPORT int VDNNF0RT_Configure(int sampleRate, int hopSize, int windowSize, const char* modelFn, void* VDNNF0RT);


  ///////////////////////////////////////////
  ///// PROCESS
  ///////////////////////////////////////////

  /**
   Call this function to perform a process step sending a window of samples and receiving the pitch value. Note
   that the pitch value received is the one from a window in the past, use the GetTotalSamplesLatency function 
   to compensate process latency accurately. 
   @param input : float buffer with input samples in the range [-1,1]
   @param nSamples : number of samples in input samples buffer
   @param pitchValue : pointer to float parameter where the extracted pitch value will be written
   @param pitchConfidence : pointer to float parameter where the extracted pitch confidence value will be written
   @param pitch_in_cents : 0 for returning the pitch in Hz, 1 for returning the pitch in cents
   @param VDNNF0RT : pointer to VDNNF0RT object instance, created in VDNNF0RT_Create()

   @return : 0 if ok, < 0 if error
  */
  VDNNF0RT_DLLEXPORT int VDNNF0RT_DoProcess(const float* input, int nSamples, float* pitchValue, float* pitchConfidence, const int pitch_in_cents, void* VDNNF0RT);

  /**
  Call this function to perform a process sending a buffer of samples corresponding to a complete audio file and 
  receiving the pitch and confidence values for each frame (at the configured hopsize).
  @param input : float buffer with input samples in the range [-1,1]
  @param nSamples : number of samples in the input buffer
  @param pitchValues : pointer to float array where the extracted pitch values will be written
  @param pitchConfidences : pointer to float array where the extracted pitch confidence values will be written
  @param pitch_in_cents : 0 for returning the pitch in Hz, 1 for returning the pitch in cents
  @param VDNNF0RT : pointer to VDNNF0RT object instance, created in VDNNF0RT_Create()

  @return : number of pitch values in the pitch array, -1 if error
 */
  VDNNF0RT_DLLEXPORT int VDNNF0RT_DoProcessOffline(const float* input, int nSamples, float* pitchValues, float* pitchConfidences, const int pitch_in_cents, void* VDNNF0RT);


  /**
   Function to output internal process latency. Don't use this function as it is not accurate to compensate 
   latency between input samples and extracted output pitch values.
   
   @param VDNNF0RT : pointer to VDNNF0RT object instance, created in VDNNF0RT_Create()

   @return : latency in number of hopsizes
  */
  VDNNF0RT_DLLEXPORT int VDNNF0RT_GetAnalysisLatency(void* VDNNF0RT);

  /**
   Function to output total latency in samples between input samples audio and extracted output pitch values.

   @param VDNNF0RT : pointer to VDNNF0RT object instance, created in VDNNF0RT_Create()

   @return : latency in number of samples between input audio and output f0 values
  */
  VDNNF0RT_DLLEXPORT int VDNNF0RT_GetTotalSamplesLatency(void* VDNNF0RT);

  /**
   Function to output number of output f0 frames that will be computed with the doProcessOffline funtion 
   for a certain number of input samples. This function is used to know in advance how many items to allocate
   for the f0 and confidence arrays before calling the doProcessOffline function. You need to configure the 
   library before calling this function to know the input samplingrate that will be used.

   @param nSamples : number of input samples that will be used for the offline process.
   @param VDNNF0RT : pointer to VDNNF0RT object instance, created in VDNNF0RT_Create()

   @return : latency in number of samples between input audio and output f0 values
  */
  VDNNF0RT_DLLEXPORT int VDNNF0RT_GetNumOutputFramesForInputSamples(int nSamples, void* VDNNF0RT);

  ///////////////////////////////////////////
  ///// VERSIONING //////////////////////////
  ///////////////////////////////////////////

  /**
   To get library version information

   @return : library version string (const char*)
  */
  VDNNF0RT_DLLEXPORT const char* VDNNF0RT_GetVersion();

  /**
   To get library version information (to be used in unity)

   @return : library version string (char*)
  */
  VDNNF0RT_DLLEXPORT char* VDNNF0RT_GetVer();

  /**
   To get library version information (to be used in android)

   @param versioninfo : string to be filled with version info

   @return : size of chars filled in version info, < 0 if error
  */
  VDNNF0RT_DLLEXPORT int32_t VDNNF0RT_GetVersionInfo(char* versioninfo);


#ifdef __cplusplus
}
#endif //__cplusplus

#endif //__VODNNF0RTLIB__