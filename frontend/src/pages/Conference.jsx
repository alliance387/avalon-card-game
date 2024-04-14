import { selectPeers, useHMSStore } from "@100mslive/react-sdk";
import { useEffect, useState } from "react";
import Peer from "./Peer";
import {battleField, evil_dudes} from "../data/players";

function Conference() {
  const peers = useHMSStore(selectPeers);

  const [gameStage, setGameStage] = useState("");
  const [filteredPeers, setFilteredPeers] = useState(peers);

  const [main_focus_peer, set_main_focus_peers] = useState({});
  const [decision_array , set_decision_array] = useState({});

  useEffect(() => {
    let unfocused = peers.map(peer => peer.id).filter(peer_id => !(peer_id in main_focus_peer))[0];
    if (unfocused !== undefined){
      set_main_focus_peers(prevState => ({
        ...prevState,
        [unfocused]: unfocused
      }));
      set_decision_array(prevState => ({
        ...prevState,
        [unfocused]: false
      }));
    }
  }, [peers]);

  function changeMainFocus(peer_id, my_peer_id) {
    set_main_focus_peers(prevState => ({
      ...prevState,
      [my_peer_id]: peer_id
    }));
  }

  const changeDecision = (peer_id) => {
    if (peers.filter(peer => peer.id === peer_id && peer.isLocal).length !== 0){
      set_decision_array(prevState => ({
        ...prevState,
        [peer_id]: !decision_array[peer_id]
      }));
    }
  }

  useEffect(() => {
    if (gameStage === "") {
      if (Object.values(decision_array).filter((status) => status == true).length >= 5){
        // TODO axios to start game
        setGameStage("Evil");
        alert('1');
      }
    }
    
  }, [decision_array]);

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
    }
    
  }, [gameStage]);

  useEffect(() => {
    setFilteredPeers(peers);
  }, [peers]);
  


  return (
    <div className="conference-section">
      {filteredPeers.filter(peer => peer.isLocal).length !== 0 ? (<>
      <div className="peers-container-main">
        
          {filteredPeers.filter(outer_peer => outer_peer.id == main_focus_peer[peers.filter(peer => peer.isLocal)[0].id]).map(peer => (
            <div className="main-item">
            <Peer key={peer.id} peer={peer} is_selected={decision_array[peer.id]} changeDecision={changeDecision}/> 
            </div>
          ))}
        </div>
        <div className="peers-container-siteitem">
          {
            filteredPeers.filter(peer => peer.id !=  main_focus_peer[peers.filter(peer => peer.isLocal)[0].id]).map(peer => (
              <div className="item" onClick={() => changeMainFocus(peer.id, peers.filter(peer => peer.isLocal)[0].id)}>
                <Peer key={peer.id} peer={peer} is_selected={decision_array[peer.id]} changeDecision={changeDecision}/>
              </div>
            ))
          }
         
      </div>
      </>): <></>}
    </div>
  );
}

export default Conference;
