import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { HMSRoomProvider } from "@100mslive/react-sdk";

import App from "./App";

const rootElement = ReactDOM.createRoot(document.getElementById("root"));
rootElement.render(
  <StrictMode>
    <HMSRoomProvider>
      <App />
    </HMSRoomProvider>
  </StrictMode>
);
