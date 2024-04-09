import { selectPeers, useHMSStore } from "@100mslive/react-sdk";
import Peer from "./Peer";

function Conference() {
  const peers = useHMSStore(selectPeers);

  return (
    <div className="conference-section">
      <div className="peers-container-main">
      {peers.map((peer) => (
<Peer key={peer.id} peer={peer} />
))}
      </div>
      <div className="peers-container-siteitem">
        <div>
        {peers.map((peer) => (
<Peer key={peer.id} peer={peer} />
))}
      </div>
        <div>
        {peers.map((peer) => (
<Peer key={peer.id} peer={peer} />
))}
      </div>
      </div>
    </div>
  );
}

export default Conference;
