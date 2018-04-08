import { h } from 'preact';
import { route } from 'preact-router';
import { View, Mask } from 'mdbreact';
import style from './style';

export default ({ tmdb_id, slug, poster_url, title }) => (
    <div className={ `${style.poster_container} mr-auto` }>
        <View zoom onClick={ () => route(`/movies/${tmdb_id}/${slug}`) }>
            <img
                src={ poster_url }
                className={ `${style.poster} img-fluid` }
                alt={ title }
            />
            <Mask className="flex-center">
                <p className="white-text">{ title }</p>
            </Mask>
        </View>
    </div>
);
