import {
	selectIsConnectedToRoom,
	useHMSActions,
	useHMSStore
} from "@100mslive/react-sdk";
import React from "react";

function Header() {
	const isConnected = useHMSStore(selectIsConnectedToRoom);
	const hmsActions = useHMSActions();

	return (
		<header>
			<img
				className="logo"
				src="https://avalon78.ca/wp-content/uploads/2021/06/logo.png"
				alt="logo"
				width="7%"
			/>
			{isConnected && (
				<button
					id="leave-btn"
					className="btn-danger"
					onClick={() => hmsActions.leave()}
				>
					Leave Room
				</button>
			)}
		</header>
	);
}

export default Header;
  