import JoinForm from "./JoinForm";
import "../styles.css";
import Conference from "./Conference";
import { useEffect, useState } from "react";
import {
  selectIsConnectedToRoom,
  useHMSActions,
  useHMSStore
} from "@100mslive/react-sdk";
import Footer from "./Footer";
import { useAuth } from "../provider/authProvider";

export default function MainWindow() {
  const { token, localEmail } = useAuth();
  const isConnected = useHMSStore(selectIsConnectedToRoom);
  const hmsActions = useHMSActions();

  const [gameId, setGameId] = useState(0);

  useEffect(() => {
    window.onunload = () => {
      if (isConnected) {
        hmsActions.leave();
      }
    };
  }, [hmsActions, isConnected]);

  return (
  <>
      {isConnected ? (
        <>
          <Conference gameId={gameId}/>
          <Footer />
        </>
      ) : (
        <JoinForm token={token} localEmail={localEmail} setGameId={setGameId}/>
      )}
      </>
  );
}