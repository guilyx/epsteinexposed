// Credits: Erwin Lejeune — 2026-02-22
import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout";
import MarkdownPage from "./components/MarkdownPage";

import homeContent from "../content/index.md?raw";
import gettingStartedContent from "../content/getting-started.md?raw";
import clientContent from "../content/api/client.md?raw";
import asyncClientContent from "../content/api/async-client.md?raw";
import modelsContent from "../content/api/models.md?raw";
import exceptionsContent from "../content/api/exceptions.md?raw";
import deploymentContent from "../content/deployment.md?raw";

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<MarkdownPage content={homeContent} />} />
        <Route path="getting-started" element={<MarkdownPage content={gettingStartedContent} />} />
        <Route path="api/client" element={<MarkdownPage content={clientContent} />} />
        <Route path="api/async-client" element={<MarkdownPage content={asyncClientContent} />} />
        <Route path="api/models" element={<MarkdownPage content={modelsContent} />} />
        <Route path="api/exceptions" element={<MarkdownPage content={exceptionsContent} />} />
        <Route path="deployment" element={<MarkdownPage content={deploymentContent} />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
