import React, {Component, useState, useEffect} from 'react'
import {Map, InfoWindow, Marker, GoogleApiWrapper} from 'google-maps-react';
import { getLoc, sendSms, getNumbers, getConfirmation, delConfirmation, getDetails } from "../api/criminalapi";
import '../App.css'
// import { checkout } from '../../../projbackend/routes/criminal';


const AlertAutomate =() => {

  const [values, setFormValues] = useState({
      message: "Click on this link to acknowledge : ", 
      messageSente: "",  
      asp:"",
      dsp:"",
      pi:"",
      trueFlag: false,
      flag: true,
      secondFlag: false,
      dataConfirm: true,
      smsSend2Flag: true,  
})
const {message,pi, asp, dsp, trueFlag, flag, secondFlag, dataConfirm, smsSend2Flag, messageSent} = values;

  const timeLapse = () => {

        getNumbers()
        .then(data => {
          console.log(data)
          setFormValues({...values,  asp: data[0].asp, dsp: data[0].dsp, pi: data[0].pi})
        })

        
  }

  useEffect(() => {
    timeLapse();
    
  }, []);

  console.log(asp)

  const smsSend =()=>{
    if(flag && (pi !== "")){

      sendSms({number: pi, message})
        .then(data => {
            console.log("successfully sent to PI's")
            console.log(data)
            setFormValues({...values, message: "Click on this link to acknowledge : ", messageSent: "Sms is sent successfully to Police Inspectors's", flag: false, secondFlag: true})
        })
    }
  }


  const afterFirstSend = () => {
    if(secondFlag){
      console.log("Im am running")
      getConfirmation()
      .then(data => {
        console.log(data)
        let check = 0
        for(let i = 0; i< data.length; i++){
          if(data[i].confirm){
            console.log(data[i].confirm)
            check = 1
            break
            // setFormValues({...values, secondFlag: false, dataConfirm: false}) 
          }
        }
        if(check === 1){
          setFormValues({...values, secondFlag: false, dataConfirm: true}) 
          delConfirmation()
          .then(data=>{console.log(data)})
          .catch(error=>{
          console.log(error)
        })
        }else if(check === 0){
          setFormValues({...values, secondFlag: false, dataConfirm: false}) 
        }
      })
    }
  }

  const smsSend2 =()=>{
    console.log(dataConfirm)
    if(smsSend2Flag && !dataConfirm && (asp !== "")){
        sendSms({number: asp, message})
                .then(data => {
                    console.log("successfully sent to ASP's")
                    console.log(data)
                     setFormValues({...values, message: "Click on this link to acknowledge : ", messageSent: "Sms is sent successfully to Assistant Superintendent of Police's", dataConfirm: true, smsSend2Flag: false})
                })
    } 
    }
    console.log(flag)
    return(
      <div>
        {flag && smsSend()}
        {/* {window.setInterval(afterFirstSend, 10000)} */}
        {secondFlag && window.setTimeout(afterFirstSend, 15000)}
        {smsSend2Flag && window.setTimeout(smsSend2,3000) }
        <div className="text-center bg-success mt-5">
          
          <h3 className="text-white">{messageSent}</h3>
          {/* <button className="btn btn-dark" onClick={smsSend}>df</button> */}
        </div>
      </div>
      
  )
}

export class MapContainer extends Component {

  constructor(props) {
    super(props);

    this.state = {
      resData: [],
      latitude:"",
      longitude: "",
      timestamp:"",
      isOpen: false,
      markerFlag: false
    }
  }

  displayMarkers = () => {
    let animate = this.props.google.maps.Animation.BOUNCE
    return this.state.resData.map((data, index) => {
      if(data.state === true){
        return <Marker animation={animate} key={index} id={index} position={{
                        lat: data._latitude,
                        lng: data._longitude
                      }}
                      onClick={() => 
                        this.setState({timestamp: JSON.stringify(data.timestamp), latitude: data._latitude, longitude: data._longitude , isOpen: true})
                        } />
      }
    })
  }

   componentDidMount(){
    getLoc().then(resData => {
      console.log(resData)
      console.log(JSON.stringify(resData))
      this.setState({resData: resData}) 
    })
    
  };

  onInfoWindowClose = () => {
    return this.setState({isOpen: false})
  }

  onTrackButton = () => {

    return this.setState({markerFlag: true})
  }
    
  
    render() {
      console.log(this.state.resData)
      console.log(this.state.selectedPlace)
      console.log(this.state.markerFlag)
      if(this.state.markerFlag){
        // getNumbers()
        // .then(data => {
        //   console.log(data)
        //   // this.setState({numbers: data[0]})
        // })
        // getConfirmation()
        // .then(data=>{
        //   console.log(data)
        // })
      //   setInterval(function() { 
      //       console.log("hello")
      //       sendSms({number , message})
      //       .then(data => {
      //           // if(data.error){
      //           //     return console.log(`Sms not sent, ${data.error}`)
      //           // }
      //           console.log("successfully sent")
      //           console.log(data)
      //           setValues({number: "", message: "", success: true, successMessage: "Sms is sent successfully"})
      //       })

      // }, 2000);
      }
      
      return (
        <div>
          <div className="mb-5 display-4 text-white" style={{color: "#aad0d9"}}>
              <b>JATAYU tracks</b>
          </div>
          <div className="row justify-content-center mb-5 ">
                            
                            <button className="mapBtn btn btn-outline-warning btn-lg px-4 ml-3 mb-5 mapBtn"  onClick={this.onTrackButton}>Start tracking</button>
                    </div>
            {this.state.markerFlag && <AlertAutomate/> }

          <Map google={this.props.google} zoom={5} initialCenter={{
            lat: 28.6706,
            lng: 94.9104
          }}>
            {this.state.markerFlag && this.displayMarkers()}


            {this.state.isOpen && <InfoWindow position={{ lat: this.state.latitude, lng: this.state.longitude}} visible={true} onClose={this.onInfoWindowClose}>
              <div>
                <h1>Time : {this.state.timestamp}</h1>
              </div>
            </InfoWindow>}
   
            
        </Map>
        </div>
        
      );
    }
  }
   
  export default GoogleApiWrapper({
    apiKey: ("AIzaSyA3IsaZeZB_Dax8mE0HdrgYP_9kWvV_VRo")
  })(MapContainer)