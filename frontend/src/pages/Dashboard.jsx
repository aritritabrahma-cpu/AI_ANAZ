import { Grid, Card, CardContent, Typography } from "@mui/material";

export default function SummaryCards({ data }) {

    const healthy = data.filter(api => api.priority === "P5").length;
    const p1 = data.filter(api => api.priority === "P1").length;
    const p2 = data.filter(api => api.priority === "P2").length;

    let avg = 0;

    if (data.length > 0) {

        avg =
            data.reduce(
                (sum, api) => sum + api.response_time,
                0
            ) / data.length;

        avg = avg.toFixed(2);

    }

    return (

        <Grid container spacing={2} sx={{ mt: 2 }}>

            <Grid item xs={12} md={3}>
                <Card>
                    <CardContent>
                        <Typography variant="h6">
                            Healthy APIs
                        </Typography>

                        <Typography variant="h4">
                            {healthy}
                        </Typography>

                    </CardContent>
                </Card>
            </Grid>

            <Grid item xs={12} md={3}>
                <Card>
                    <CardContent>
                        <Typography variant="h6">
                            P1 Errors
                        </Typography>

                        <Typography variant="h4">
                            {p1}
                        </Typography>

                    </CardContent>
                </Card>
            </Grid>

            <Grid item xs={12} md={3}>
                <Card>
                    <CardContent>
                        <Typography variant="h6">
                            P2 Errors
                        </Typography>

                        <Typography variant="h4">
                            {p2}
                        </Typography>

                    </CardContent>
                </Card>
            </Grid>

            <Grid item xs={12} md={3}>
                <Card>
                    <CardContent>
                        <Typography variant="h6">
                            Avg Response
                        </Typography>

                        <Typography variant="h4">
                            {avg} ms
                        </Typography>

                    </CardContent>
                </Card>
            </Grid>

        </Grid>

    );

}