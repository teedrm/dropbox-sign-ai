import "@passageidentity/passage-elements/passage-auth";
import React from 'react';
function Home() {
    return (
        <passage-auth app-id={import.meta.env.VITE_REACT_APP_PASSAGE_APP_ID}></passage-auth>
    );
}


export default Home;