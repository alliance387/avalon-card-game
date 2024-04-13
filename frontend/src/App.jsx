import JoinForm from "./JoinForm";
import Header from "./Header";
import "./styles.css";
import Conference from "./Conference";
import { useEffect } from "react";
import {
  selectIsConnectedToRoom,
  useHMSActions,
  useHMSStore
} from "@100mslive/react-sdk";

import AuthProvider from "./provider/authProvider";
import Routes from "./routes";

import Footer from "./Footer";

export default function App() {
  const isConnected = useHMSStore(selectIsConnectedToRoom);
  const hmsActions = useHMSActions();

  // useEffect(() => {
  //   window.onunload = () => {
  //     if (isConnected) {
  //       hmsActions.leave();
  //     }
  //   };
  // }, [hmsActions, isConnected]);

  return (
    <AuthProvider>
      
      <div className="App">
      <Header />
      <Routes />
      {/* {isConnected ? (
        <>
          <Conference />
          <Footer />
        </>
      ) : (
        <JoinForm />
      )} */}
    </div>
    </AuthProvider>

  );
}
