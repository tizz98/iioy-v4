import { h } from 'preact';
import { Container } from 'mdbreact';
import Loader from '../loader';
import Poster from '../movies/poster';

export default ({ movies, maxWidth = '300px' }) => (
    <Container>
        { !movies && <Loader className="mt-3" /> }
        <div className="d-flex justify-content-start align-items-start flex-wrap">
            {
                movies && movies.map(movie => (
                    <Poster
                        { ...movie }
                        key={ movie.tmdb_id }
                        maxWidth={ maxWidth }
                    />
                ))
            }
        </div>
    </Container>
);
