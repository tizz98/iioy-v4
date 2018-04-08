import { h } from 'preact';
import { route } from 'preact-router';
import { View, Mask } from 'mdbreact';
import PosterImage from './poster-image';
import style from './style';

export default ({ tmdb_id, slug, poster_url, title, maxWidth = '300px' }) => (
    <div className={ `${style.poster_container} mr-auto ml-auto` }>
        <View zoom onClick={ () => route(`/movies/${tmdb_id}/${slug}`) }>
            <PosterImage poster_url={ poster_url } title={ title } maxWidth={ maxWidth } />
            <Mask className="flex-center text-center">
                <p className="white-text">{ title }</p>
            </Mask>
        </View>
    </div>
);
