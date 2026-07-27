import { Grid, Card, CardContent, Typography } from "@mui/material";

export default function SummaryCards({ data }) {

    return (

        <Grid container spacing={2} sx={{ mt: 2 }}>

            <Grid item xs={12} md={3}>
                <Card>
                    <CardContent>
                        <Typography variant="h6">
                            Healthy APIs
                        </Typography>

                        <Typography variant="h4">
                            {data.length}
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
                            -
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
                            -
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
                            -
                        </Typography>
                    </CardContent>
                </Card>
            </Grid>

        </Grid>

    );

}