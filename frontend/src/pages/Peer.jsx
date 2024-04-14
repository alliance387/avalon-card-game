import { useVideo } from "@100mslive/react-sdk";

function Peer({ peer, is_selected, changeDecision }) {
  const { videoRef } = useVideo({
    trackId: peer.videoTrack
  });
  return (
    <div className="peer-container">
      <img class ="button-start"src={is_selected ? "gold_coin.png" : "grey_coin.png"} alt="" width="10%" onClick={() => changeDecision(peer.id)}/>
      
      <img class ="img-role"src={"Oberon.jpg"} alt="" width="10%"/>

      <video
        ref={videoRef}
        className={`peer-video ${peer.isLocal ? "local" : ""}`}
        autoPlay
        muted
        playsInline
      />
      <div className="peer-name">
        {peer.name} {peer.isLocal ? "(You)" : ""}
      </div>
    </div>
  );
}

export default Peer;
