import {
    Grid,
    Card,
    CardContent,
    Typography,
    Box
} from "@mui/material";

import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import SpeedIcon from "@mui/icons-material/Speed";

export default function SummaryCards({ data = [] }) {

    const healthy = data.filter(api => api.priority === "P5").length;
    const p1 = data.filter(api => api.priority === "P1").length;
    const p2 = data.filter(api => api.priority === "P2").length;

    const avg =
        data.length > 0
            ? (
                data.reduce(
                    (sum, api) => sum + Number(api.response_time || 0),
                    0
                ) / data.length
            ).toFixed(2)
            : "0.00";

    const total = data.length || 1;

    const cards = [
        {
            title: "Healthy APIs",
            value: healthy,
            subtitle: `${((healthy / total) * 100).toFixed(1)}%`,
            icon: <CheckCircleIcon sx={{ fontSize: 40 }} />,
            bg: "#E8F5E9",
            color: "#2E7D32"
        },
        {
            title: "P1 Errors",
            value: p1,
            subtitle: `${((p1 / total) * 100).toFixed(1)}%`,
            icon: <WarningAmberIcon sx={{ fontSize: 40 }} />,
            bg: "#FFF8E1",
            color: "#F57C00"
        },
        {
            title: "P2 Errors",
            value: p2,
            subtitle: `${((p2 / total) * 100).toFixed(1)}%`,
            icon: <ErrorIcon sx={{ fontSize: 40 }} />,
            bg: "#FDECEA",
            color: "#D32F2F"
        },
        {
            title: "Avg Response",
            value: `${avg} ms`,
            subtitle: "Average",
            icon: <SpeedIcon sx={{ fontSize: 40 }} />,
            bg: "#E3F2FD",
            color: "#1565C0"
        }
    ];

    return (
        <Grid container spacing={3} sx={{ mt: 2 }}>

            {cards.map((card, index) => (

                <Grid item xs={12} sm={6} md={3} key={index}>

                    <Card
                        sx={{
                            borderRadius: 3,
                            backgroundColor: card.bg,
                            transition: "0.3s",
                            "&:hover": {
                                transform: "translateY(-6px)",
                                boxShadow: 6
                            }
                        }}
                    >

                        <CardContent>

                            <Box
                                display="flex"
                                justifyContent="space-between"
                                alignItems="center"
                            >

                                <Box>

                                    <Typography
                                        variant="body2"
                                        color="text.secondary"
                                    >
                                        {card.title}
                                    </Typography>

                                    <Typography
                                        variant="h4"
                                        fontWeight="bold"
                                        sx={{ color: card.color }}
                                    >
                                        {card.value}
                                    </Typography>

                                    <Typography
                                        variant="caption"
                                        color="text.secondary"
                                    >
                                        {card.subtitle}
                                    </Typography>

                                </Box>

                                <Box sx={{ color: card.color }}>
                                    {card.icon}
                                </Box>

                            </Box>

                        </CardContent>

                    </Card>

                </Grid>

            ))}

        </Grid>
    );
}
