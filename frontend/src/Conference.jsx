import { selectPeers, useHMSStore } from "@100mslive/react-sdk";
import Peer from "./Peer";

function Conference() {
  const peers = useHMSStore(selectPeers);

  return (
    <div className="conference-section">
      <h2>Conference</h2>
      <div className="peers-container-main">
        {peers.map((peer) => (
          <Peer key={peer.id} peer={peer} />
        ))}
      </div>
      <div className="peers-container-siteitem">
      </div>
    </div>
  );
}

export default Conference;
