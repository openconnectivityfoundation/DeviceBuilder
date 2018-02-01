//******************************************************************
//
// Copyright 2017 Open Connectivity Foundation
//
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#include <signal.h>
#include <thread>
#include <functional>
#include <string>
#include <iostream>
#include <memory>
#include <exception> 

#ifdef HAVE_WINDOWS_H
#include <windows.h>
#endif

#include "ocstack.h"
#include "OCPlatform.h"
#include "OCApi.h"
#include "ocpayload.h"

using namespace OC;
namespace PH = std::placeholders;

/*
 tool_version          : 20171123
 input_file            : ../device_output/out_codegeneration_merged.swagger.json
 version of input_file : v1.1.0-20160519
 title of input_file   : Binary Switch
*/


#define INTERFACE_KEY "if"

// Set of strings for each of platform Info fields
std::string gPlatformId = "0A3E0D6F-DBF5-404E-8719-D6880042463A";
std::string gManufacturerName = "ocf";
std::string gManufacturerLink = "https://ocf.org/";
std::string gModelNumber = "ModelNumber";
std::string gDateOfManufacture = "2017-12-01";
std::string gPlatformVersion = "1.0";
std::string gOperatingSystemVersion = "myOS";
std::string gHardwareVersion = "1.0";
std::string gFirmwareVersion = "1.0";
std::string gSupportLink = "https://ocf.org/";
std::string gSystemTime = "2017-12-01T12:00:00.52Z";

// Set of strings for each of device info fields
std::string  gDeviceName = "Binary Switch";
std::string  gDeviceType = "oic.d.light";
std::string  gSpecVersion = "ocf.1.0.0";
//std::vector<std::string> gDataModelVersions = {"ocf.res.1.1.0", "ocf.sh.1.1.0"};
#pragma warning( push ) 
#pragma warning( disable : 4592)
std::vector<std::string> gDataModelVersions = {"ocf.res.1.3.0", "ocf.sh.1.3.0"};
//std::vector<std::string> gDataModelVersions = {"ocf.res.1.3.0", "ocf.dev.1.3.0"};
#pragma warning( pop )

std::string  gProtocolIndependentID = "fa008167-3bbf-4c9d-8604-c9bcb96cb712";
// OCPlatformInfo Contains all the platform info to be stored
OCPlatformInfo platformInfo;

// forward declarations
void DeletePlatformInfo();
void initializePlatform();
OCStackResult SetDeviceInfo();
OCStackResult SetPlatformInfo(std::string platformID, std::string manufacturerName,
        std::string manufacturerUrl, std::string modelNumber, std::string dateOfManufacture,
        std::string platformVersion, std::string operatingSystemVersion,
        std::string hardwareVersion, std::string firmwareVersion, std::string supportUrl,
        std::string systemTime);

/**
*  DuplicateString
*
* @param targetString  destination string, will be allocated
* @param sourceString  source string, e.g. will be copied

*  TODO: don't use strncpy
*/
void DuplicateString(char ** targetString, std::string sourceString)
{
    *targetString = new char[sourceString.length() + 1];
    strncpy(*targetString, sourceString.c_str(), (sourceString.length() + 1));
}

/*
* default class, so that we have to define less variables/functions.
*/
class Resource
{
    protected:
    OCResourceHandle m_resourceHandle;
    OCRepresentation m_rep;
    virtual OCEntityHandlerResult entityHandler(std::shared_ptr<OCResourceRequest> request)=0;
};


  

class c_binaryswitchResource : public Resource
{
    public:
        /*
        * constructor
        */
        c_binaryswitchResource()
        {
            std::cout << "- Running: c_binaryswitchResource constructor" << std::endl;
            std::string resourceURI = "/binaryswitch";
            
            // initialize member variables /binaryswitch
            m_var_value_value = true; // current value of property "value" 
            
            
             
            
            
            
            
             
            // initialize vector if
            
            m_var_value_if.push_back("oic.if.baseline"); 
            m_var_value_if.push_back("oic.if.a"); 
            
            
            
            
            m_var_value_n = "";  // current value of property "n"  
            
            
            
            
             
            // initialize vector rt
            
            m_var_value_rt.push_back("oic.r.switch.binary"); 
            
        
            EntityHandler cb = std::bind(&c_binaryswitchResource::entityHandler, this,PH::_1);
            //uint8_t resourceProperty = 0;
            OCStackResult result = OCPlatform::registerResource(m_resourceHandle,
                resourceURI,
                m_RESOURCE_TYPE[0],
                m_RESOURCE_INTERFACE[0],
                cb,
                OC_DISCOVERABLE | OC_OBSERVABLE | OC_SECURE );
                
            // add the additional interfaces
            std::cout << "\t" << "# resource interfaces: " << m_nr_resource_interfaces << std::endl;
            std::cout << "\t" << "# resource types     : " << m_nr_resource_types << std::endl;
            for( int a = 1; a < m_nr_resource_interfaces; a++)
            {
                OCStackResult result1 = OCBindResourceInterfaceToResource(m_resourceHandle, m_RESOURCE_INTERFACE[a].c_str());
                if (result1 != OC_STACK_OK)
                    std::cerr << "Could not bind interface:" << m_RESOURCE_INTERFACE[a] << std::endl;
            }
            // add the additional resource types
            for( int a = 1; a < m_nr_resource_types; a++ )
            {
                OCStackResult result2 = OCBindResourceTypeToResource(m_resourceHandle, m_RESOURCE_TYPE[a].c_str());
                if (result2 != OC_STACK_OK)
                    std::cerr << "Could not bind resource type:" << m_RESOURCE_INTERFACE[a] << std::endl;
            }    

            if(OC_STACK_OK != result)
            {
                throw std::runtime_error(
                    std::string("c_binaryswitchResource failed to start")+std::to_string(result));
            }
        }
    private:
     
        /*
        * function to make the payload for the retrieve function (e.g. GET) /binaryswitch
        * @param queries  the query parameters for this call
        */
        OCRepresentation get(QueryParamsMap queries)
        {        
            
            m_rep.setValue(m_var_name_value, m_var_value_value );  
            m_rep.setValue(m_var_name_if,  m_var_value_if );  
            m_rep.setValue(m_var_name_n, m_var_value_n );  
            m_rep.setValue(m_var_name_rt,  m_var_value_rt ); 
        
            return m_rep;
        }
     
        /*
        * function to parse the payload for the update function (e.g. POST) /binaryswitch
        * @param queries  the query parameters for this call
        * @param rep  the response to get the property values from
        * @return OCEntityHandlerResult ok or not ok indication
        */
        OCEntityHandlerResult post(QueryParamsMap queries, const OCRepresentation& rep)
        {
            OCEntityHandlerResult ehResult = OC_EH_OK;
            
            try {
                if (rep.hasAttribute(m_var_name_value))
                {
                    // value exist in payload
                    
                }  
            }
            catch (std::exception& e)
            {
                std::cout << e.what() << std::endl;
            } 
             
             
             
             
            // TODO add check on array contents out of range, etc..
            
            if (ehResult == OC_EH_OK)
            {
                // no error: assign the variables
                
                try {
                    if (rep.getValue(m_var_name_value, m_var_value_value ))
                    {
                        std::cout << "\t\t" << "property 'value': " << m_var_value_value << std::endl;
                    }
                    else
                    {
                        std::cout << "\t\t" << "property 'value' not found in the representation" << std::endl;
                    }
                }
                catch (std::exception& e)
                {
                    std::cout << e.what() << std::endl;
                }
             
                // array only works for integer, boolean, numbers and strings
                // TODO: make it also work with array of objects
                try {
                    if (rep.hasAttribute(m_var_name_if))
                    {
                        rep.getValue(m_var_name_if, m_var_value_if);
                        int first = 1;
                        std::cout << "\t\t" << "property 'if' : " ;
                        for(auto myvar: m_var_value_if)
                        {
                            if(first)
                            {
                                std::cout << myvar;
                                first = 0;
                            }
                            else
                            {
                                std::cout << "," << myvar;
                            }
                        }
                        std::cout <<  std::endl;
                    }
                    else
                    {
                        std::cout << "\t\t" << "property 'if' not found in the representation" << std::endl;
                    }
                }
                catch (std::exception& e)
                {
                    std::cout << e.what() << std::endl;
                }
             
                try {
                    if (rep.getValue(m_var_name_n, m_var_value_n ))
                    {
                        std::cout << "\t\t" << "property 'n' : " << m_var_value_n << std::endl;
                    }
                    else
                    {
                        std::cout << "\t\t" << "property 'n' not found in the representation" << std::endl;
                    }
                }
                catch (std::exception& e)
                {
                    std::cout << e.what() << std::endl;
                }
             
                // array only works for integer, boolean, numbers and strings
                // TODO: make it also work with array of objects
                try {
                    if (rep.hasAttribute(m_var_name_rt))
                    {
                        rep.getValue(m_var_name_rt, m_var_value_rt);
                        int first = 1;
                        std::cout << "\t\t" << "property 'rt' : " ;
                        for(auto myvar: m_var_value_rt)
                        {
                            if(first)
                            {
                                std::cout << myvar;
                                first = 0;
                            }
                            else
                            {
                                std::cout << "," << myvar;
                            }
                        }
                        std::cout <<  std::endl;
                    }
                    else
                    {
                        std::cout << "\t\t" << "property 'rt' not found in the representation" << std::endl;
                    }
                }
                catch (std::exception& e)
                {
                    std::cout << e.what() << std::endl;
                }
            
            }            
            return ehResult;            
        }
    // resource types and interfaces as array..
        std::string m_RESOURCE_TYPE[1] = {"oic.r.switch.binary"}; // rt value (as an array)
        std::string m_RESOURCE_INTERFACE[2] = {"oic.if.baseline","oic.if.a"}; // interface if (as an array) 
        std::string m_IF_UPDATE[3] = {"oic.if.a", "oic.if.rw", "oic.if.baseline"}; // updateble interfaces
        int m_nr_resource_types = 1;
        int m_nr_resource_interfaces = 2;
        ObservationIds m_interestedObservers;        
        
        // member variables for path: /binaryswitch
        bool m_var_value_value; // the value for the attribute
        std::string m_var_name_value = "value"; // the name for the attribute
        
        
        std::vector<std::string>  m_var_value_if;
        std::string m_var_name_if = "if"; // the name for the attribute
        
        std::string m_var_value_n; // the value for the attribute
        std::string m_var_name_n = "n"; // the name for the attribute
        
        
        std::vector<std::string>  m_var_value_rt;
        std::string m_var_name_rt = "rt"; // the name for the attribute
        protected:
        /*
        * function to check if the interface is
        * @param  interface_name the interface name used during the request
        * @return true: updatable interface
        */
        bool in_updatable_interfaces(std::string interface_name)
        {
            for (int i=0; i<3; i++)
            {
                if (m_IF_UPDATE[i].compare(interface_name) == 0)
                    return true;
            }
            return false;
        }
    
        /*
        * the entity handler for this resource
        * @param request the incoming request to handle
        * @return OCEntityHandlerResult ok or not ok indication
        */
        virtual OCEntityHandlerResult entityHandler(std::shared_ptr<OCResourceRequest> request)
        {
            OCEntityHandlerResult ehResult = OC_EH_ERROR;
            //std::cout << "In entity handler for c_binaryswitchResource " << std::endl;
                          
            if(request)
            {
                std::cout << "In entity handler for c_binaryswitchResource, URI is : "
                          << request->getResourceUri() << std::endl;
                          
                // Check for query params (if any)
                QueryParamsMap queries = request->getQueryParameters();
                if (!queries.empty())
                {
                    std::cout << "\nQuery processing up to entityHandler" << std::endl;
                }
                for (auto it : queries)
                {
                    std::cout << "Query key: " << it.first << " value : " << it.second
                            << std::endl;
                } 
                // get the value, so that we can AND it to check which flags are set
                int requestFlag = request->getRequestHandlerFlag();                

                if(requestFlag & RequestHandlerFlag::RequestFlag)
                {
                    // request flag is set
                    auto pResponse = std::make_shared<OC::OCResourceResponse>();
                    pResponse->setRequestHandle(request->getRequestHandle());
                    pResponse->setResourceHandle(request->getResourceHandle());

                    if(request->getRequestType() == "GET")
                    {
                        std::cout<<"c_binaryswitchResource Get Request"<< std::endl;

                        pResponse->setResourceRepresentation(get(queries), "");
                        if(OC_STACK_OK == OCPlatform::sendResponse(pResponse))
                        {
                            ehResult = OC_EH_OK;
                        }
                    }
     
                    else if(request->getRequestType() == "POST")
                    {
                        std::cout <<"c_binaryswitchResource Post Request"<<std::endl;
                        bool  handle_post = true; 

                        if (queries.size() > 0)
                        {
                            for (const auto &eachQuery : queries)
                            {
                                std::string key = eachQuery.first;
                                if (key.compare(INTERFACE_KEY) == 0)
                                {
                                    std::string value = eachQuery.second;
                                    if (in_updatable_interfaces(value) == false)
                                    {
                                        std::cout << "Update request received via interface: " << value
                                                    << " . This interface is not authorized to update resource!!" << std::endl;
                                        pResponse->setResponseResult(OCEntityHandlerResult::OC_EH_FORBIDDEN);
                                        handle_post = false;
                                        ehResult = OC_EH_ERROR;
                                        break;
                                    }
                                }
                            }
                        }
                        if (handle_post)
                        {
                            ehResult = post(queries, request->getResourceRepresentation());
                            if (ehResult == OC_EH_OK)
                            {
                                pResponse->setResourceRepresentation(get(queries), "");
                            }
                            else
                            {
                                 pResponse->setResponseResult(OCEntityHandlerResult::OC_EH_ERROR);
                            }
                            if(OC_STACK_OK == OCPlatform::sendResponse(pResponse))
                            {                                
                                // TODO: if there are observers inform the observers
                                //OCStackResult sResult;
                                // update all observers with the new value
                                // not sure if this is an blocking call
                                //sResult = OCPlatform::notifyListOfObservers(   m_resourceHandle,
                                //                                               m_interestedObservers,
                                //                                               pResponse);
                            }
                        }
                    }
                    else
                    {
                        std::cout << "c_binaryswitchResource unsupported request type (delete,put,..)"
                            << request->getRequestType() << std::endl;
                        pResponse->setResponseResult(OC_EH_ERROR);
                        OCPlatform::sendResponse(pResponse);
                        ehResult = OC_EH_ERROR;
                    }
                }
                
                if(requestFlag & RequestHandlerFlag::ObserverFlag)
                {
                    // observe flag is set
                    std::cout << "\t\trequestFlag : Observer\n" << std::endl;
                    ObservationInfo observationInfo = request->getObservationInfo();
                    if(ObserveAction::ObserveRegister == observationInfo.action)
                    {
                        // add observer
                        m_interestedObservers.push_back(observationInfo.obsId);
                    }
                    else if(ObserveAction::ObserveUnregister == observationInfo.action)
                    {
                        // delete observer
                        m_interestedObservers.erase(std::remove(
                                                                    m_interestedObservers.begin(),
                                                                    m_interestedObservers.end(),
                                                                    observationInfo.obsId),
                                                                    m_interestedObservers.end());
                    } 
                    ehResult = OC_EH_OK;                    
                }
            }
            return ehResult;
        }
};
  

class c_dimmingResource : public Resource
{
    public:
        /*
        * constructor
        */
        c_dimmingResource()
        {
            std::cout << "- Running: c_dimmingResource constructor" << std::endl;
            std::string resourceURI = "/dimming";
            
            // initialize member variables /dimming
            
            
            
             
            // initialize vector if
            
            m_var_value_if.push_back("oic.if.baseline"); 
            m_var_value_if.push_back("oic.if.a"); 
            
            
            
            
            m_var_value_n = "";  // current value of property "n"  
            
            
            
            
             
            // initialize vector rt
            
            m_var_value_rt.push_back("oic.r.light.dimming"); 
            
            
            
            m_var_value_dimmingSetting = 0; // current value of property "dimmingSetting" 
             
            
        
            EntityHandler cb = std::bind(&c_dimmingResource::entityHandler, this,PH::_1);
            //uint8_t resourceProperty = 0;
            OCStackResult result = OCPlatform::registerResource(m_resourceHandle,
                resourceURI,
                m_RESOURCE_TYPE[0],
                m_RESOURCE_INTERFACE[0],
                cb,
                OC_DISCOVERABLE | OC_OBSERVABLE | OC_SECURE );
                
            // add the additional interfaces
            std::cout << "\t" << "# resource interfaces: " << m_nr_resource_interfaces << std::endl;
            std::cout << "\t" << "# resource types     : " << m_nr_resource_types << std::endl;
            for( int a = 1; a < m_nr_resource_interfaces; a++)
            {
                OCStackResult result1 = OCBindResourceInterfaceToResource(m_resourceHandle, m_RESOURCE_INTERFACE[a].c_str());
                if (result1 != OC_STACK_OK)
                    std::cerr << "Could not bind interface:" << m_RESOURCE_INTERFACE[a] << std::endl;
            }
            // add the additional resource types
            for( int a = 1; a < m_nr_resource_types; a++ )
            {
                OCStackResult result2 = OCBindResourceTypeToResource(m_resourceHandle, m_RESOURCE_TYPE[a].c_str());
                if (result2 != OC_STACK_OK)
                    std::cerr << "Could not bind resource type:" << m_RESOURCE_INTERFACE[a] << std::endl;
            }    

            if(OC_STACK_OK != result)
            {
                throw std::runtime_error(
                    std::string("c_dimmingResource failed to start")+std::to_string(result));
            }
        }
    private:
     
        /*
        * function to make the payload for the retrieve function (e.g. GET) /dimming
        * @param queries  the query parameters for this call
        */
        OCRepresentation get(QueryParamsMap queries)
        {        
             
            m_rep.setValue(m_var_name_if,  m_var_value_if );  
            m_rep.setValue(m_var_name_n, m_var_value_n );  
            m_rep.setValue(m_var_name_rt,  m_var_value_rt );  
            m_rep.setValue(m_var_name_dimmingSetting, m_var_value_dimmingSetting ); 
        
            return m_rep;
        }
     
        /*
        * function to parse the payload for the update function (e.g. POST) /dimming
        * @param queries  the query parameters for this call
        * @param rep  the response to get the property values from
        * @return OCEntityHandlerResult ok or not ok indication
        */
        OCEntityHandlerResult post(QueryParamsMap queries, const OCRepresentation& rep)
        {
            OCEntityHandlerResult ehResult = OC_EH_OK;
             
             
             
             
            try {
                if (rep.hasAttribute(m_var_name_dimmingSetting))
                {
                    // allocate the variable
                    int value;
                    // get the actual value from the payload
                    rep.getValue(m_var_name_dimmingSetting, value);
            
                    // value exist in payload
                    
                    
                    
                }
            }
            catch (std::exception& e)
            {
                std::cout << e.what() << std::endl;
            } 
             
            // TODO add check on array contents out of range, etc..
            
            if (ehResult == OC_EH_OK)
            {
                // no error: assign the variables
                 
                // array only works for integer, boolean, numbers and strings
                // TODO: make it also work with array of objects
                try {
                    if (rep.hasAttribute(m_var_name_if))
                    {
                        rep.getValue(m_var_name_if, m_var_value_if);
                        int first = 1;
                        std::cout << "\t\t" << "property 'if' : " ;
                        for(auto myvar: m_var_value_if)
                        {
                            if(first)
                            {
                                std::cout << myvar;
                                first = 0;
                            }
                            else
                            {
                                std::cout << "," << myvar;
                            }
                        }
                        std::cout <<  std::endl;
                    }
                    else
                    {
                        std::cout << "\t\t" << "property 'if' not found in the representation" << std::endl;
                    }
                }
                catch (std::exception& e)
                {
                    std::cout << e.what() << std::endl;
                }
             
                try {
                    if (rep.getValue(m_var_name_n, m_var_value_n ))
                    {
                        std::cout << "\t\t" << "property 'n' : " << m_var_value_n << std::endl;
                    }
                    else
                    {
                        std::cout << "\t\t" << "property 'n' not found in the representation" << std::endl;
                    }
                }
                catch (std::exception& e)
                {
                    std::cout << e.what() << std::endl;
                }
             
                // array only works for integer, boolean, numbers and strings
                // TODO: make it also work with array of objects
                try {
                    if (rep.hasAttribute(m_var_name_rt))
                    {
                        rep.getValue(m_var_name_rt, m_var_value_rt);
                        int first = 1;
                        std::cout << "\t\t" << "property 'rt' : " ;
                        for(auto myvar: m_var_value_rt)
                        {
                            if(first)
                            {
                                std::cout << myvar;
                                first = 0;
                            }
                            else
                            {
                                std::cout << "," << myvar;
                            }
                        }
                        std::cout <<  std::endl;
                    }
                    else
                    {
                        std::cout << "\t\t" << "property 'rt' not found in the representation" << std::endl;
                    }
                }
                catch (std::exception& e)
                {
                    std::cout << e.what() << std::endl;
                }
             
                try {
                    // value exist in payload
                    if (rep.getValue(m_var_name_dimmingSetting, m_var_value_dimmingSetting ))
                    {
                        std::cout << "\t\t" << "property 'dimmingSetting': " << m_var_value_dimmingSetting << std::endl;
                    }
                    else
                    {
                        std::cout << "\t\t" << "property 'dimmingSetting' not found in the representation" << std::endl;
                    }
                }
                catch (std::exception& e)
                {
                    std::cout << e.what() << std::endl;
                }
            
            }            
            return ehResult;            
        }
    // resource types and interfaces as array..
        std::string m_RESOURCE_TYPE[1] = {"oic.r.light.dimming"}; // rt value (as an array)
        std::string m_RESOURCE_INTERFACE[2] = {"oic.if.baseline","oic.if.a"}; // interface if (as an array) 
        std::string m_IF_UPDATE[3] = {"oic.if.a", "oic.if.rw", "oic.if.baseline"}; // updateble interfaces
        int m_nr_resource_types = 1;
        int m_nr_resource_interfaces = 2;
        ObservationIds m_interestedObservers;        
        
        // member variables for path: /dimming
        
        std::vector<std::string>  m_var_value_if;
        std::string m_var_name_if = "if"; // the name for the attribute
        
        std::string m_var_value_n; // the value for the attribute
        std::string m_var_name_n = "n"; // the name for the attribute
        
        
        std::vector<std::string>  m_var_value_rt;
        std::string m_var_name_rt = "rt"; // the name for the attribute
        
        int m_var_value_dimmingSetting; // the value for the attribute
        std::string m_var_name_dimmingSetting = "dimmingSetting"; // the name for the attribute
        protected:
        /*
        * function to check if the interface is
        * @param  interface_name the interface name used during the request
        * @return true: updatable interface
        */
        bool in_updatable_interfaces(std::string interface_name)
        {
            for (int i=0; i<3; i++)
            {
                if (m_IF_UPDATE[i].compare(interface_name) == 0)
                    return true;
            }
            return false;
        }
    
        /*
        * the entity handler for this resource
        * @param request the incoming request to handle
        * @return OCEntityHandlerResult ok or not ok indication
        */
        virtual OCEntityHandlerResult entityHandler(std::shared_ptr<OCResourceRequest> request)
        {
            OCEntityHandlerResult ehResult = OC_EH_ERROR;
            //std::cout << "In entity handler for c_dimmingResource " << std::endl;
                          
            if(request)
            {
                std::cout << "In entity handler for c_dimmingResource, URI is : "
                          << request->getResourceUri() << std::endl;
                          
                // Check for query params (if any)
                QueryParamsMap queries = request->getQueryParameters();
                if (!queries.empty())
                {
                    std::cout << "\nQuery processing up to entityHandler" << std::endl;
                }
                for (auto it : queries)
                {
                    std::cout << "Query key: " << it.first << " value : " << it.second
                            << std::endl;
                } 
                // get the value, so that we can AND it to check which flags are set
                int requestFlag = request->getRequestHandlerFlag();                

                if(requestFlag & RequestHandlerFlag::RequestFlag)
                {
                    // request flag is set
                    auto pResponse = std::make_shared<OC::OCResourceResponse>();
                    pResponse->setRequestHandle(request->getRequestHandle());
                    pResponse->setResourceHandle(request->getResourceHandle());

                    if(request->getRequestType() == "GET")
                    {
                        std::cout<<"c_dimmingResource Get Request"<< std::endl;

                        pResponse->setResourceRepresentation(get(queries), "");
                        if(OC_STACK_OK == OCPlatform::sendResponse(pResponse))
                        {
                            ehResult = OC_EH_OK;
                        }
                    }
     
                    else if(request->getRequestType() == "POST")
                    {
                        std::cout <<"c_dimmingResource Post Request"<<std::endl;
                        bool  handle_post = true; 

                        if (queries.size() > 0)
                        {
                            for (const auto &eachQuery : queries)
                            {
                                std::string key = eachQuery.first;
                                if (key.compare(INTERFACE_KEY) == 0)
                                {
                                    std::string value = eachQuery.second;
                                    if (in_updatable_interfaces(value) == false)
                                    {
                                        std::cout << "Update request received via interface: " << value
                                                    << " . This interface is not authorized to update resource!!" << std::endl;
                                        pResponse->setResponseResult(OCEntityHandlerResult::OC_EH_FORBIDDEN);
                                        handle_post = false;
                                        ehResult = OC_EH_ERROR;
                                        break;
                                    }
                                }
                            }
                        }
                        if (handle_post)
                        {
                            ehResult = post(queries, request->getResourceRepresentation());
                            if (ehResult == OC_EH_OK)
                            {
                                pResponse->setResourceRepresentation(get(queries), "");
                            }
                            else
                            {
                                 pResponse->setResponseResult(OCEntityHandlerResult::OC_EH_ERROR);
                            }
                            if(OC_STACK_OK == OCPlatform::sendResponse(pResponse))
                            {                                
                                // TODO: if there are observers inform the observers
                                //OCStackResult sResult;
                                // update all observers with the new value
                                // not sure if this is an blocking call
                                //sResult = OCPlatform::notifyListOfObservers(   m_resourceHandle,
                                //                                               m_interestedObservers,
                                //                                               pResponse);
                            }
                        }
                    }
                    else
                    {
                        std::cout << "c_dimmingResource unsupported request type (delete,put,..)"
                            << request->getRequestType() << std::endl;
                        pResponse->setResponseResult(OC_EH_ERROR);
                        OCPlatform::sendResponse(pResponse);
                        ehResult = OC_EH_ERROR;
                    }
                }
                
                if(requestFlag & RequestHandlerFlag::ObserverFlag)
                {
                    // observe flag is set
                    std::cout << "\t\trequestFlag : Observer\n" << std::endl;
                    ObservationInfo observationInfo = request->getObservationInfo();
                    if(ObserveAction::ObserveRegister == observationInfo.action)
                    {
                        // add observer
                        m_interestedObservers.push_back(observationInfo.obsId);
                    }
                    else if(ObserveAction::ObserveUnregister == observationInfo.action)
                    {
                        // delete observer
                        m_interestedObservers.erase(std::remove(
                                                                    m_interestedObservers.begin(),
                                                                    m_interestedObservers.end(),
                                                                    observationInfo.obsId),
                                                                    m_interestedObservers.end());
                    } 
                    ehResult = OC_EH_OK;                    
                }
            }
            return ehResult;
        }
};


class IoTServer
{
    public:
        /**
        *  constructor
        *  creates all resources from the resource classes.
        */
        IoTServer()
            :
    m_binaryswitchInstance(),
    m_dimmingInstance()
    
        {
            std::cout << "Running IoTServer constructor" << std::endl;
            initializePlatform();
        }

        /**
        *  destructor
        *
        */
        ~IoTServer()
        {
            std::cout << "Running IoTServer destructor" << std::endl;
            DeletePlatformInfo();
        }
    
    private:
  
        c_binaryswitchResource  m_binaryswitchInstance;
  
        c_dimmingResource  m_dimmingInstance;
};


/**
*  intialize platform
*  initializes the oic/p resource
*/
void initializePlatform()
{
    std::cout << "Running initializePlatform" << std::endl;
    
    // initialize "oic/p"
    
    std::cout << "oic/p" << std::endl;
    OCStackResult result = SetPlatformInfo(gPlatformId, gManufacturerName, gManufacturerLink,
            gModelNumber, gDateOfManufacture, gPlatformVersion, gOperatingSystemVersion,
            gHardwareVersion, gFirmwareVersion, gSupportLink, gSystemTime);
    result = OCPlatform::registerPlatformInfo(platformInfo);
    if (result != OC_STACK_OK)
    {
        std::cout << "Platform Registration (oic/p) failed\n";
    }
    
    // initialize "oic/d"
    std::cout << "oic/d" << std::endl;
    result = SetDeviceInfo();
    if (result != OC_STACK_OK)
    {
        std::cout << "Device Registration (oic/p) failed\n";
    }
}


/**
*  DeletePlatformInfo
*  Deletes the allocated platform information
*/
void DeletePlatformInfo()
{
    delete[] platformInfo.platformID;
    delete[] platformInfo.manufacturerName;
    delete[] platformInfo.manufacturerUrl;
    delete[] platformInfo.modelNumber;
    delete[] platformInfo.dateOfManufacture;
    delete[] platformInfo.platformVersion;
    delete[] platformInfo.operatingSystemVersion;
    delete[] platformInfo.hardwareVersion;
    delete[] platformInfo.firmwareVersion;
    delete[] platformInfo.supportUrl;
    delete[] platformInfo.systemTime;
}

/**
*  SetPlatformInfo 
*  Sets the platform information ("oic/p"), from the globals

* @param platformID the platformID
* @param manufacturerName the manufacturerName
* @param manufacturerUrl the manufacturerUrl
* @param modelNumber the modelNumber
* @param platformVersion the platformVersion
* @param operatingSystemVersion the operatingSystemVersion
* @param hardwareVersion the hardwareVersion
* @param firmwareVersion the firmwareVersion
* @param supportUrl the supportUrl
* @param systemTime the systemTime
* @return OC_STACK_ERROR or OC_STACK_OK
*/
OCStackResult SetPlatformInfo(std::string platformID, std::string manufacturerName,
        std::string manufacturerUrl, std::string modelNumber, std::string dateOfManufacture,
        std::string platformVersion, std::string operatingSystemVersion,
        std::string hardwareVersion, std::string firmwareVersion, std::string supportUrl,
        std::string systemTime)
{
    DuplicateString(&platformInfo.platformID, platformID);
    DuplicateString(&platformInfo.manufacturerName, manufacturerName);
    DuplicateString(&platformInfo.manufacturerUrl, manufacturerUrl);
    DuplicateString(&platformInfo.modelNumber, modelNumber);
    DuplicateString(&platformInfo.dateOfManufacture, dateOfManufacture);
    DuplicateString(&platformInfo.platformVersion, platformVersion);
    DuplicateString(&platformInfo.operatingSystemVersion, operatingSystemVersion);
    DuplicateString(&platformInfo.hardwareVersion, hardwareVersion);
    DuplicateString(&platformInfo.firmwareVersion, firmwareVersion);
    DuplicateString(&platformInfo.supportUrl, supportUrl);
    DuplicateString(&platformInfo.systemTime, systemTime);

    return OC_STACK_OK;
}

/**
*  SetDeviceInfo
*  Sets the device information ("oic/d"), from the globals

* @return OC_STACK_ERROR or OC_STACK_OK
*/
OCStackResult SetDeviceInfo()
{
    OCStackResult result = OC_STACK_ERROR;

    OCResourceHandle handle = OCGetResourceHandleAtUri(OC_RSRVD_DEVICE_URI);
    if (handle == NULL)
    {
        std::cout << "Failed to find resource " << OC_RSRVD_DEVICE_URI << std::endl;
        return result;
    }
    result = OCBindResourceTypeToResource(handle, gDeviceType.c_str());
    if (result != OC_STACK_OK)
    {
        std::cout << "Failed to add device type" << std::endl;
        return result;
    }
    result = OCPlatform::setPropertyValue(PAYLOAD_TYPE_DEVICE, OC_RSRVD_DEVICE_NAME, gDeviceName);
    if (result != OC_STACK_OK)
    {
        std::cout << "Failed to set device name" << std::endl;
        return result;
    }
    result = OCPlatform::setPropertyValue(PAYLOAD_TYPE_DEVICE, OC_RSRVD_DATA_MODEL_VERSION,
                                          gDataModelVersions);
    if (result != OC_STACK_OK)
    {
        std::cout << "Failed to set data model versions" << std::endl;
        return result;
    }
    result = OCPlatform::setPropertyValue(PAYLOAD_TYPE_DEVICE, OC_RSRVD_SPEC_VERSION, gSpecVersion);
    if (result != OC_STACK_OK)
    {
        std::cout << "Failed to set spec version" << std::endl;
        return result;
    }
    result = OCPlatform::setPropertyValue(PAYLOAD_TYPE_DEVICE, OC_RSRVD_PROTOCOL_INDEPENDENT_ID,
                                          gProtocolIndependentID);
    if (result != OC_STACK_OK)
    {
        std::cout << "Failed to set piid" << std::endl;
        return result;
    }

    return OC_STACK_OK;
}
/**
*  server_fopen
*  opens file
*  implements redirection to open:
* - initial security settings
* - introspection file
* @param path path+filename of the file to open
* @param mode mode of the file to open
* @return the filehandle of the opened file (or error)
*/
FILE* server_fopen(const char* path, const char* mode)
{
    FILE* fileptr = NULL;

    if (0 == strcmp(path, OC_SECURITY_DB_DAT_FILE_NAME))
    {
        // reading the security initial setup file
        fileptr = fopen("server_security.dat", mode);
        std::cout << "reading security file 'server_security.dat' ptr: " << fileptr << std::endl;
        return fileptr;
    }
    else if (0 == strcmp(path, OC_INTROSPECTION_FILE_NAME))
    {
        // reading the introspection file
        fileptr = fopen("server_introspection.dat", mode);
        std::cout << "reading introspection file  'server_introspection.dat' ptr: " << fileptr << std::endl;
        return fileptr;
    }
    else
    {
        std::cout << "persistent storage - server_fopen: " << path << std::endl;
        return fopen(path, mode);
    }
}


#ifdef LINUX
// global needs static, otherwise it can be compiled out and then Ctrl-C does not work
static int quit = 0;
// handler for the signal to stop the application
void handle_signal(int signal)
{
    quit = 1;
}
#endif

// main application
// starts the server 
int main()
{
    // Create persistent storage handlers
    OCPersistentStorage ps{server_fopen, fread, fwrite, fclose, unlink};
    // create the platform
    PlatformConfig cfg
    {
        ServiceType::InProc,
        ModeType::Server,
        &ps
    };
    OCPlatform::Configure(cfg);
    OC_VERIFY(OCPlatform::start() == OC_STACK_OK);
    
    std::cout << "device type: " <<  gDeviceType << std::endl;
    std::cout << "platformID: " <<  gPlatformId << std::endl;
    std::cout << "platform independent: " <<  gProtocolIndependentID << std::endl;


#ifdef LINUX
    struct sigaction sa;
    sigfillset(&sa.sa_mask);
    sa.sa_flags = 0;
    sa.sa_handler = handle_signal;
    sigaction(SIGINT, &sa, NULL);
    std::cout << "Press Ctrl-C to quit...." << std::endl;
    // create the server
    IoTServer server;
    do
    {
        usleep(2000000);
    }
    while (quit != 1);
    // delete the server
    delete IoTServer;
#endif
    
    
#if defined(_WIN32)
    IoTServer server;
    std::cout << "Press Ctrl-C to quit...." << std::endl;
    // we will keep the server alive for at most 30 minutes
    std::this_thread::sleep_for(std::chrono::minutes(30));
    OC_VERIFY(OCPlatform::stop() == OC_STACK_OK);
#endif    
    
    return 0;
}
