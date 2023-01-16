import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';

export function ProgramHeader() {
    return (<Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        alignSelf="center">
        <AppBar position="relative" style={{ "background-image": "linear-gradient(to bottom right, #A26CF4, #7941FB, #442f65)" }}>
        <Toolbar>
            <Typography variant="h2" sx={{ flexGrow: 1 }}>
            Virus Crawler
            </Typography>
        </Toolbar>
        </AppBar>
    </Box>)
}