import React from 'react';
import styles from './home.module.css'
import imageUv from '../assets/img1.jpeg'
import imageOutdoor from '../assets/img2.jpeg'

const Home = () => {
    return (
        <div className={ styles.main }>
            <img className={ styles.img_uv } src={imageUv} alt="img Uv" />
            <p className={ `text-center f_bold ${ styles.title }` }>Outdoor UV exposure</p>
            <p className={ `text-center ${ styles.desc }` }>How to protect yourself from Sun</p>
            <img className={ styles.img_outdoor } src={imageOutdoor} alt="img Uv" />
        </div>
    )
};

export default Home;