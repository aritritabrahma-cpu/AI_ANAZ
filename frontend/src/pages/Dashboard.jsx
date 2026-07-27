import { useEffect, useState } from "react";
import { Container } from "@mui/material";

import Navbar from "../components/Navbar";
import SummaryCards from "../components/SummaryCards";
import ApiTable from "../components/ApiTable";
import AIInsights from "../components/AIInsights";

import { fetchApiData } from "../services/api";

export default function Dashboard() {

    const [data, setData] = useState([]);

    useEffect(() => {

        async function loadData() {

            try {

                const result = await fetchApiData();

                setData(result);

            } catch (err) {

                console.error(err);

            }

        }

        loadData();

        const interval = setInterval(loadData, 3000);

        return () => clearInterval(interval);

    }, []);

    return (

        <>
            <Navbar />

            <Container maxWidth="xl">

                <SummaryCards data={data} />

                <ApiTable data={data} />

                <AIInsights data={data} />

            </Container>

        </>

    );

}