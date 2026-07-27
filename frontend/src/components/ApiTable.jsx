import { Paper, Typography } from "@mui/material";

export default function ApiTable({ data }) {

    return (

        <Paper sx={{ mt: 3, p: 2 }}>

            <Typography variant="h6">
                Live API Status
            </Typography>

            <pre>

                {JSON.stringify(data, null, 2)}

            </pre>

        </Paper>

    );

}