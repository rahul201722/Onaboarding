import React from 'react';
import styles from './about.module.css'

const About = () => {
    return (
        <main>
            <h1 className={styles.title}>What do we do ?</h1>
            <p className={styles.desc}>
            At Uv Protection,We are a team focused on the collection and analysis of
            ultraviolet index in Australia, committed to providing users with accurate 
            UV intensity information and scientific outdoor skin protection recommendations. 
            By monitoring UV data across Australia in real time, we help users understand current 
            UV intensity levels and provide personalised sun protection guidelines.
            We are well aware of the potential damage of UV rays to skin health, 
            so we hope to help every user better protect themselves and enjoy
            outdoor activities while protecting themselves from UV
            rays through professional data and practical advice.
            </p>
        </main>
    )
};

export default About;