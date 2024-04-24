import JoinForm from "./JoinForm";
import "../mobile-styles.css";
import Conference from "./Conference";
import { useEffect } from "react";
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
          <Conference />
          <Footer />
        </>
      ) : (
        <JoinForm token={token} localEmail={localEmail}/>
      )}
      </>
  );
}