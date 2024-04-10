import { selectPeers, useHMSStore } from "@100mslive/react-sdk";
import { useEffect, useState } from "react";
import Peer from "./Peer";

function Conference() {
  const peers = useHMSStore(selectPeers);

  const [main_focus_peer, set_main_focus_peers] = useState({});

  useEffect(() => {
    let unfocused = peers.map(peer => peer.id).filter(peer_id => !(peer_id in main_focus_peer))[0];
    if (unfocused !== undefined){
      set_main_focus_peers(prevState => ({
        ...prevState,
        [unfocused]: unfocused
      }));
    }
  }, [peers]);

  return (
    <div className="conference-section">
      <div className="peers-container-main">
        {peers.filter(outer_peer => outer_peer.id == main_focus_peer[peers.filter(peer => peer.isLocal)[0].id]).map(peer => (
          <Peer key={peer.id} peer={peer} />
        ))}
      {/* {peers.map((peer) => (
<Peer key={peer.id} peer={peer} />
))} */}
      </div>
      <div className="peers-container-siteitem">
        {
          peers.filter(peer => peer.id !=  main_focus_peer[peers.filter(peer => peer.isLocal)[0].id]).map(peer => (
            <div>
              <Peer key={peer.id} peer={peer} />
            </div>
          ))
        }
      </div>
    </div>
  );
}

export default Conference;
