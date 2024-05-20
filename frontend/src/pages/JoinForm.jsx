import axios from "axios";
import { useHMSActions } from "@100mslive/react-sdk";
import { useState, useEffect } from "react";
import { useAuth } from "../provider/authProvider";
import { useNavigate } from "react-router-dom";

const API_URL = "https://avalon-card-game.onrender.com";

function Join({token, localEmail}) {

  const hmsActions = useHMSActions();
  const [inputValues, setInputValues] = useState({
    userName: "",
    token: ""
  });
  const handleInputChange = (e) => {
    setInputValues((prevValues) => ({
      ...prevValues,
      [e.target.name]: e.target.value
    }));
  };

  const navigate = useNavigate();

  const [sessionRooms, setSessionRooms] = useState([]);

  const enterToRoom = async (room_code) => {
    const authToken = await hmsActions.getAuthTokenByRoomCode({ roomCode: room_code });
    try {
      axios({method: 'post', url: API_URL + `/game/enter_room`, params: {room_code: room_code, user_email: localEmail}})
      .then((response) => {
        if (response.data.event === 'enter' || response.data.event === 'reenter'){
          navigate(`/room/${room_code}`, { replace: true });
          hmsActions.join({ userName: localEmail, authToken})
        }
      });
    } catch(e){
      console.log(e);
    }
  }
  const handleSubmit = async (e) => {
    e.preventDefault();
    const { 
      userName = '',
      roomCode = '',
    } = inputValues;
    // use room code to fetch auth token
    const authToken = await hmsActions.getAuthTokenByRoomCode({ roomCode });
  
    try { 
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      axios({method: 'post', url: API_URL + `/session`, params: {room_code: roomCode, user_email: localEmail}, headers:{"Authorization" : `Bearer ${token}`, 'accept': 'application/json'}})
      .then((response) => {
        console.log(response.data);
      }).catch(e => {
        console.log(e);
      }).then(() => {
        axios({method: 'post', url: API_URL + `/game/enter_room`, params: {room_code: roomCode, user_email: localEmail}})
        .then((response) => {
          if (response.data.event === 'enter' || response.data.event === 'reenter'){
            navigate(`/room/${roomCode}`, { replace: true });
            hmsActions.join({ userName: localEmail, authToken})
          }
        })
        
      });
      
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    if(axios.defaults.headers.common["Authorization"] === ""){
      return
    }
    else{
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      axios.get(API_URL + `/session`, {params: {'user_email': localEmail}})
      .then((response) => {
        console.log(response);
        setSessionRooms(response.data);
        
      }).catch(e => {
        console.log(e);
      });
    }
    
  }, []);

  return (
    <>
    <form className="join-form" onSubmit={handleSubmit}>
      <h2>Join Room</h2>
      <div className="input-container">
        <input 
          id="room-code" 
          type="text"
          name="roomCode"
          placeholder="Room code"
          onChange={handleInputChange}
        />
      </div>
      <button className="btn-primary" >Join</button>
    </form>
    <div className="join-form">
      <h2>Last Sessions</h2>
      <br />
      {sessionRooms.map(room => (
        <h2 key={room.id} onClick={async () => enterToRoom(room.code)}>Room #{room.room_id}</h2>
      ))}
      
    </div>
    </>
  );
}

export default Join;