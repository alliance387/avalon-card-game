import { selectPeers, useHMSStore } from "@100mslive/react-sdk";
import { useEffect, useState } from "react";
import Peer from "./Peer";

function Conference() {
  const peers = useHMSStore(selectPeers);

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


  return (
    <div className="conference-section">
      <div className="peers-container-main">
        {peers.filter(outer_peer => outer_peer.id == main_focus_peer[peers.filter(peer => peer.isLocal)[0].id]).map(peer => (
          <div className="main-item">
          <Peer key={peer.id} peer={peer} is_selected={decision_array[peer.id]} changeDecision={changeDecision}/>
          </div>
        ))}
      </div>
      <div className="peers-container-siteitem">
        {
          peers.filter(peer => peer.id !=  main_focus_peer[peers.filter(peer => peer.isLocal)[0].id]).map(peer => (
            <div className="item" onClick={() => changeMainFocus(peer.id, peers.filter(peer => peer.isLocal)[0].id)}>
              <Peer key={peer.id} peer={peer} is_selected={decision_array[peer.id]} changeDecision={changeDecision}/>
            </div>
          ))
        }
      </div>
    </div>
  );
}

export default Conference;
