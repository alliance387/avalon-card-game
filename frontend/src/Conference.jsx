import { selectPeers, useHMSStore } from "@100mslive/react-sdk";
import Peer from "./Peer";

function Conference() {
  const peers = useHMSStore(selectPeers);

  return (
    <div className="conference-section">
      <div className="peers-container-main">
      <img
				className="logo"
				src="https://avalon78.ca/wp-content/uploads/2021/06/logo.png"
				alt="logo"
				width="7%"
			/>
      </div>
      <div className="peers-container-siteitem">
        <div>
          <img
				className="logo"
				src="https://avalon78.ca/wp-content/uploads/2021/06/logo.png"
				alt="logo"
				width="7%"
			/>
      </div>
        <div>
          <img
				className="logo"
				src="https://avalon78.ca/wp-content/uploads/2021/06/logo.png"
				alt="logo"
				width="7%"
			/>
      </div>
      </div>
    </div>
  );
}

export default Conference;
