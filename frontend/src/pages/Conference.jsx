import { selectPeers, useHMSStore } from "@100mslive/react-sdk";
import { useEffect, useState } from "react";
import Peer from "./Peer";
import {battleField, evil_dudes} from "../data/players";
import axios from "axios";

const API_URL = "https://avalon-card-game.onrender.com";

function Conference({gameId}) {
  const peers = useHMSStore(selectPeers);

  const [filteredPeers, setFilteredPeers] = useState(peers);

  // Getting info
  const [userInfo, setUserInfo] = useState({});
  const [gameInfo, setGameInfo] = useState({});
  useEffect(() => {
    if (gameId)
    {
      axios({method: 'get', url: API_URL + `/game/game-info`, params: {game_id: gameId}})
      .then((response) => {
        setUserInfo(response.data.active_users);
        setGameInfo(response.data.game);
      });
    }
  });
  
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
  const changeDecision = (peer) => {
    if (peer.isLocal)
    {
      axios({method: 'post', url: API_URL + `/game/change_state`, params: {game_id: gameId, user_email: peer.name}})
      .then((response) => {
        
      });
      
    }
  }

  // Stage part
  const [gameStage, setGameStage] = useState("");
  const [lockStage, setLockStage] = useState(1);
  useEffect(() => {
    if (gameStage === "") 
    {
      if (gameInfo["win"] == 2 && lockStage)
      {
        setLockStage(0);
        setFilteredPeers({});
        setTimeout(() => {
          setGameStage("Evil");
          setLockStage(1);
        }, 3000);
      }
    }
    else if (gameStage === "Evil")
    {
      if (lockStage)
      {
        setLockStage(0);
        setFilteredPeers(peers.filter(peer => evil_dudes.includes(peer.roleName) && peer.roleName !== "oberon"));
        setTimeout(() => {
          setFilteredPeers({});
          setTimeout(() => {
            setGameStage("Merlin");
            setLockStage(1);
          }, 3000);
        }, 8000);
      }
    }
    else if (gameStage === "Merlin") 
    {
      if (lockStage)
      {
        setLockStage(0);
        setFilteredPeers(peers.filter(peer => evil_dudes.includes(peer.roleName)));
        setTimeout(() => {
          setFilteredPeers({});
          setTimeout(() => {
            setGameStage("Percival");
            setLockStage(1);
          }, 3000);
        }, 8000);
      }
    }
    else if (gameStage === "Percival") {
      if (lockStage)
      {
        setLockStage(0);
        setFilteredPeers(peers.filter(peer => peer.roleName === "merlin" || peer.roleName === "morgana"));
        setTimeout(() => {
          setFilteredPeers({});
          setTimeout(() => {
            setGameStage("Game");
            setLockStage(1);
          }, 3000);
        }, 8000);
      }
    }
    else if (gameStage === "Game") {
      // Show Game

      // Polling time
      

      // After getting people

    }
    
  }, [gameInfo]);

  useEffect(() => {
    if (gameStage === "" || gameStage === "Game")
    {
      setFilteredPeers(peers);
    }
  }, [peers]);
  


  return (
    <>
    <div className="conference-section">
      {(filteredPeers.filter(peer => peer.isLocal).length !== 0 && ["", "Game", "Evil"].includes(gameStage)) || 
       (filteredPeers.filter(peer => peer.isLocal && peer.roleName === "merlin").length === 1 && gameStage === "Merlin") || 
       (filteredPeers.filter(peer => peer.isLocal && peer.roleName === "percival").length === 1 && gameStage === "Percival") ? (<>
      <div className="peers-container-main">
        
          {filteredPeers.filter(outer_peer => outer_peer.id === main_focus_peer).map(peer => (
            <div className="main-item">
            <Peer key={peer.id} peer={peer} is_selected={userInfo[peer.name] && userInfo[peer.name].state} changeDecision={changeDecision}/> 
            </div>
          ))}
        </div>
        <div className="peers-container-siteitem">
          {
            filteredPeers.filter(peer => peer.id !== main_focus_peer).map(peer => (
              <div className="item" onClick={() => changeMainFocus(peer.id)}>
                <Peer key={peer.id} peer={peer} is_selected={userInfo[peer.name] && userInfo[peer.name].state} changeDecision={changeDecision}/>
              </div>
            ))
          }
         
      </div>
      </>): <></>}
    </div>
    {/* <div className="conference-section">
      <img src="/success_mission_card.png" alt=""/>
      <img src="/fail_mission_card.png" alt="" />
    </div> */}
  </>);
}

export default Conference;
