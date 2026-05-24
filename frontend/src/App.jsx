import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LandingPage from "@/pages/LandingPage";
import SearchResultsPage from "@/pages/SearchResultsPage";
import ProductDetailPage from "@/pages/ProductDetailPage";
import NavigationPage from "@/pages/NavigationPage";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/search" element={<SearchResultsPage />} />
        <Route path="/product/:id" element={<ProductDetailPage />} />
        <Route path="/navigate/:id" element={<NavigationPage />} />
      </Routes>
    </Router>
  );
}
