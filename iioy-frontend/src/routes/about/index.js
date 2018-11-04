import { h } from 'preact';
import { Container } from 'mdbreact';
import Title from '../../components/title';
import TitleHeader, { COLORS } from '../../components/title-header';
import style from './style';
import imgV1 from '../../assets/img/iioy_v1.png';
import imgV2 from '../../assets/img/iioy_v2.png';
import imgV3 from '../../assets/img/iioy_v3.png';
import psf from '../../assets/img/psf.png';

const Link = ({ href, name, description }) => (
    <li>
        <a href={ href } target="_blank" rel="noopener noreferrer">
            { name }
        </a> - { description }
    </li>
)

export default () => (
    <div className={ style.main }>
        <Title title="About" />
        <TitleHeader
            text="About"
            color={ COLORS.peach }
        />

        <Container>
            <p className="mt-3">
                Is It Out Yet (or "IIOY" for short) is a one stop shop to see
                if your favorite movie is out yet.
            </p>
            <p>
                To get started, just type the name of the movie you're thinking of
                in the search bar on the home page and you'll see the magic right
                from the beginning. We've tried to make it as easy as possible to see
                if your favorite movie is out yet.
            </p>
            <p>
                IIOY is a <a href="http://zumh.org" target="_blank" rel="noreferrer noopener">ZUMH</a> project;
                this is the fourth major iteration fo the website. Read about why this site is rewritten every
                couple years <a href="https://medium.com/@daetam/being-a-better-programmer-917ede778206" target="_blank" rel="noreferrer noopener">here &rsaquo;</a>
            </p>

            <h3 className="h3-responsive mt-3">Credits</h3>
            <p>I would like to thank a couple projects that without them, this website wouldn't be possible.</p>

            <ul className={ style.unstyled_list }>
                <Link
                    href="http://djangoproject.com/"
                    name="Django"
                    description="The backend API powering this website."
                />
                <Link
                    href="https://mdbootstrap.com"
                    name="Material design bootstrap"
                    description="Great looking frontend framework for React."
                />
                <Link
                    href="http://www.themoviedb.org/"
                    name="TheMovieDB"
                    description="Easy to use API for all things movie related."
                />
                <Link
                    href="http://www.omdbapi.com/"
                    name="The Open Movie Database"
                    description="Phenomenal API that has grown a lot in the past years."
                />
                <Link
                    href="http://elijahwilson.me"
                    name="Me (Elijah Wilson)"
                    description="A personal plug, but I've been developing this website since 2013 and it continues to be a great programming exercise."
                />
            </ul>

            <p>Proud member of the <a href="https://psfmember.org/" target="_blank" rel="noopener noreferrer">Python Software Foundation</a></p>
            <img src={ psf } style={ { maxWidth: '300px' } } className="img-fluid" alt="Python Software Foundation" />

            <h3 className="h3-responsive mt-3">Previous versions</h3>
            <h4 className="h4-responsive mt-3">Version 3 (2015/2016)</h4>
            <img src={ imgV3 } className="img-fluid" alt="IIOY v3" />

            <h4 className="h4-responsive mt-3">Version 2 (2014/2015)</h4>
            <img src={ imgV2 } className="img-fluid" alt="IIOY v2" />

            <h4 className="h4-responsive mt-3">Version 1 (2013/2014)</h4>
            <img src={ imgV1 } className="img-fluid" alt="IIOY v1" />
        </Container>
    </div>
);
