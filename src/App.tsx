import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { ResearchProvider } from "@/context/ResearchContext";
import Home from "./pages/Home";
import Discover from "./pages/Discover";
import Clusters from "./pages/Clusters";
import Synthesis from "./pages/Synthesis";
import Gaps from "./pages/Gaps";
import Code from "./pages/Code";
import About from "./pages/About";
import NotFound from "./pages/NotFound";

const queryClient = new QueryClient();

const App = () => (
  <QueryClientProvider client={queryClient}>
    <ResearchProvider>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/discover" element={<Discover />} />
            <Route path="/clusters" element={<Clusters />} />
            <Route path="/synthesis" element={<Synthesis />} />
            <Route path="/gaps" element={<Gaps />} />
            <Route path="/code" element={<Code />} />
            <Route path="/about" element={<About />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </TooltipProvider>
    </ResearchProvider>
  </QueryClientProvider>
);

export default App;
