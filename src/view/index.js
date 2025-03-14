import React from 'react';
import styles from './index.module.css'
import imageUv from '../assets/img1.jpeg'
import imageUvMap from '../assets/img3.png'
import LineChart from '../component/LineChart';

const Index = () => {
    return (
        <main className={`${styles.main} just-between`}>
            <img src={imageUvMap} className={styles.img_uv_map} alt="uv map" />
            <section className={ `flex_wid ${ styles.content }` }>
                <img src={imageUv} className={styles.img_uv} alt="uv" />
                <LineChart />
            </section>
        </main>
    )
};

export default Index;