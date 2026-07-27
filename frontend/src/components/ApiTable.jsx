import {
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Chip,
    Typography
} from "@mui/material";

export default function ApiTable({ data = [] }) {

    return (

        <Paper sx={{ mt: 3, p: 2 }}>

            <Typography variant="h6" sx={{ mb: 2 }}>
                Live API Status
            </Typography>

            <TableContainer>

                <Table>

                    <TableHead>

                        <TableRow>

                            <TableCell><b>Page</b></TableCell>

                            <TableCell><b>API URL</b></TableCell>

                            <TableCell><b>Status</b></TableCell>

                            <TableCell><b>Priority</b></TableCell>

                            <TableCell><b>Response Time</b></TableCell>

                            <TableCell><b>Action</b></TableCell>

                        </TableRow>

                    </TableHead>

                    <TableBody>

                        {data.map((api, index) => (

                            <TableRow key={index}>

                                <TableCell>
                                    {api.page}
                                </TableCell>

                                <TableCell
                                    sx={{
                                        maxWidth: 350,
                                        wordBreak: "break-word"
                                    }}
                                >
                                    {api.api_url}
                                </TableCell>

                                <TableCell>

                                    <Chip
                                        label={api.status}
                                        color={
                                            api.status >= 500
                                                ? "error"
                                                : api.status >= 400
                                                ? "warning"
                                                : "success"
                                        }
                                    />

                                </TableCell>

                                <TableCell>

                                    <Chip
                                        label={api.priority}
                                        color={
                                            api.priority === "P2"
                                                ? "error"
                                                : api.priority === "P1"
                                                ? "warning"
                                                : "success"
                                        }
                                    />

                                </TableCell>

                                <TableCell>
                                    {api.response_time} ms
                                </TableCell>

                                <TableCell>
                                    {api.action}
                                </TableCell>

                            </TableRow>

                        ))}

                    </TableBody>

                </Table>

            </TableContainer>

        </Paper>

    );

}