import { selectPeers, useHMSStore } from "@100mslive/react-sdk";
import { useEffect, useState } from "react";
import Peer from "./Peer";
import {battleField, evil_dudes} from "../data/players";
import axios from "axios";

const API_URL = "https://avalon-card-game.onrender.com";

function Conference({gameId}) {
  const peers = useHMSStore(selectPeers);

  const [gameStage, setGameStage] = useState("");
  const [filteredPeers, setFilteredPeers] = useState(peers);

  
  

  // Focus part
  const [main_focus_peer, set_main_focus_peer] = useState("");
  useEffect(() => {
    if (main_focus_peer === "")
    {
      set_main_focus_peer(peers.filter(peer => peer.isLocal)[0].id);
    }
    else if(!main_focus_peer in peers){
      set_main_focus_peer(peers[0].id);
    }
  }, [peers]);

  function changeMainFocus(peer_id) {
    set_main_focus_peer(peer_id);
  }

  // Decision part
  const [decision, set_decision] = useState(0);
  const changeDecision = (peer) => {
    const next_value = decision === 0 ? 1 : 0;
    if (peer.isLocal)
    {
      axios({method: 'post', url: API_URL + `/game/change_state`, data: {game_id: gameId, user_email: peer.name}})
      .then((response) => {
        if (response.data.event === 'changed'){
          set_decision(next_value);
        }
      });
      
    }
  }

  useEffect(() => {
    console.log(gameId);
    if (gameStage === "") {
        // TODO axios to start game
        // setGameStage("Evil");
        // alert('1');
    }
    
  }, [decision]);

  useEffect(() => {
    if (gameStage === "Evil") {
      // Show mafia
      console.log(filteredPeers.filter(peer => evil_dudes.includes(peer.roleName)));
      setFilteredPeers(peers);
      // setFilteredPeers(filteredPeers.filter(peer => evil_dudes.includes(peer.roleName)));
      // setGameStage("Merlin");
      // alert('2');
    }
    else if (gameStage === "Merlin") {
      // Show Merlin
      setGameStage("Percival");
      alert('3');
    }
    else if (gameStage === "Percival") {
      // Show Percival
      setGameStage("Game");
      alert('4');
    }
    else if (gameStage === "Game") {
      // Show Game
      alert('5');

      // Polling time
      

      // After getting people

    }
    
  }, [gameStage]);

  useEffect(() => {
    setFilteredPeers(peers);
  }, [peers]);
  


  return (
    <>
    <div className="conference-section">
      {filteredPeers.filter(peer => peer.isLocal).length !== 0 ? (<>
      <div className="peers-container-main">
        
          {filteredPeers.filter(outer_peer => outer_peer.id === main_focus_peer).map(peer => (
            <div className="main-item">
            <Peer key={peer.id} peer={peer} is_selected={decision} changeDecision={changeDecision}/> 
            </div>
          ))}
        </div>
        <div className="peers-container-siteitem">
          {
            filteredPeers.filter(peer => peer.id !== main_focus_peer).map(peer => (
              <div className="item" onClick={() => changeMainFocus(peer.id)}>
                <Peer key={peer.id} peer={peer} is_selected={decision} changeDecision={changeDecision}/>
              </div>
            ))
          }
         
      </div>
      </>): <></>}
    </div>
    <div className="conference-section">
      <img src="/success_mission_card.png" alt=""/>
      <img src="/fail_mission_card.png" alt="" />
    </div>
  </>);
}

export default Conference;
