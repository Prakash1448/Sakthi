import { BrowserRouter, Routes, Route } from "react-router-dom";

import Home from "./pages/Home";
import CameraSetup from "./pages/CameraSetup";
import Interview from "./pages/Interview";
import Result from "./pages/Result";
import Dashboard from "./pages/Dashboard";

function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<Home />}
                />

                <Route
                    path="/dashboard"
                    element={<Dashboard />}
                />

                <Route
                    path="/camera-setup"
                    element={<CameraSetup />}
                />

                <Route
                    path="/interview"
                    element={<Interview />}
                />

                <Route
                    path="/result"
                    element={<Result />}
                />

            </Routes>

        </BrowserRouter>

    );

}

export default App;