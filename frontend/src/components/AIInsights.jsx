import { Paper, Typography } from "@mui/material";

export default function AIInsights({ data }) {

    return (

        <Paper sx={{ mt: 3, p: 2 }}>

            <Typography variant="h6">

                AI Insights

            </Typography>

            <Typography sx={{ mt: 2 }}>

                APIs Received : {data.length}

            </Typography>

        </Paper>

    );

}