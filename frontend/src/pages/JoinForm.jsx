import axios from "axios";
import { useHMSActions } from "@100mslive/react-sdk";
import { useState, useEffect } from "react";
import { useAuth } from "../provider/authProvider";

const API_URL = "https://avalon-card-game.onrender.com";

function Join() {
  const { token, localEmail } = useAuth();

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

  const [sessionRooms, setSessionRooms] = useState([]);

  const enterToRoom = async (room_code) => {
    const authToken = await hmsActions.getAuthTokenByRoomCode({ roomCode: room_code });
    try {
      await hmsActions.join({ userName: localEmail, authToken});
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
      axios({method: 'post', url: API_URL + `/session`, params: {room_code: roomCode, user_email: localEmail}, headers:{"Authorization" : `Bearer ${token}`, 'accept': 'application/json'}})
      .then((response) => {
        console.log(response.data);
      }).catch(e => {
        console.log(e);
      });
      await hmsActions.join({ userName: localEmail, authToken});
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
      axios.get(API_URL + `/session`, {params: {'user_email': localEmail}}, {headers: {"Authorization" : `Bearer ${token}`, 'accept': 'application/json'}})
      .then((response) => {
        console.log(response.data);
        setSessionRooms(response.data);
      }).catch(e => {
        console.log(e);
      });
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
