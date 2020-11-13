# ADRs

## Python and BeautifulSoup4 for Extracting Old Website Data
1. **Summary** – In order to obtain all info that must be migrated from the old
site to the new site, we decided to extract that info from the old site files
using Python 3 and BeautifulSoup4.
2. **Problem** – Our problem is finding a way to use the old text chapters,
images, excavation maps, and other content, and also completely update the
interface to support features that the old site simply does not (such as
navigation by page number). Because of the numerous hyperlinks to images,
citations, and other content contained within the old site, we need to extract
all that information from the old site, and cannot just create a new site and
copy the book chapters over.
3. **Constraints** – Because of the complex nature of the old files (file
names, hyperlinks, directory structure, etc.), anything purely manual such as
WordPress or copying the text on each page is out of the question. Because the
client wants a well-designed updated interface, we also need a tool that can
deal with and clean up the various frames that store all the info in the old
site. We also need flexibility to deal with issues like missing &lt;/p&gt;
closing tags.
4. **Options**
    1. *BeautifulSoup*, a Python library for web scraping. Pros include high
    flexibility and adaptability, ability to use other Python libraries to
    perform unit tests, ease of working with local files (since our clients
    provided us with all of the site files), lots of documentation, and
    familiarity with Python by all team members. Cons include the need to
    automate the parsing for our site specifically (i.e. no plug and play).
    2. *ParseHub*, a desktop app for web scraping. Pros include ease of plug
    and play and predefined data storage. Cons include storing info on their
    web servers, a fixed definition based on their software for how to store
    the data, and a limit on the number of web pages scraped.
    3. *Selenium*, a browser automation suite that supports usage for web
    scraping. Pros include extreme freedom in choice of programming language
    (Java, Python, C#, Ruby, JavaScript), and lots of support. Cons include
    relative complexity and dependence on WebDriver to drive a browser –
    meaning potentially significant downgrades in speed when running the code
    compared to just a BeautifulSoup script.
    4. *Construct our own web scrapers using Python or JavaScript.* Pros
    include complete freedom. Cons include needing to build up a lot of
    groundwork for reading documents, finding tags, and extracting info from
    those tags.
5. **Rationale** – We went with BeautifulSoup4 + Python, because all of our
team members were familiar with Python and so would not have to worry as much
about the learning curve. It also simplifies reading HTML documents much more
compared to building it all from scratch ourselves; we do not have to worry
about any privacy or copyright issues; and once our extraction code is built,
it will be easy for our clients or future site editors to tweak and re-run the
code if needed. The code should also be fairly fast to run, making it easier to
debug or tweak.


## Using JSON Rather than Databases for Storing Extracted Data
1. **Summary** – In order to store the data we extract from the old website for
use when generating the new site, we decided to store the data in files of JSON
format.
2. **Problem** – We need to persistently store extracted data, and be able to
process it later when generating the website. This allows us to separate the
extraction and generation parts of the code, making them easier to think about
logically and in terms of maintaining. We also need to support the processing
of any data that we extract, such as converting paragraphs to Markdown or
turning hyperlinks to old pages into new links. Thus, we need to decide on a
specific format to store the data in.
3. **Constraints** – The data storage format needs to also be relatively easy
to use in the code that generates the new site. It also needs to be highly
structured and flexible due to how each page in the old site can be classified
into one of several specific types, with specific formatting for all of them.
It also needs to be easy to go back in and change hyperlinks or specific
components, depending on what we need to make the new pages. As this is a
highly technical question, the client does not have strong preferences on this.
4. **Options** –
    1. *JSON*. Pros include extreme flexibility and ease of use, support by
    numerous free libraries (including in Python), no need to learn any
    language for using a database, and easy translation between Python
    dictionaries and JSON objects. Cons include lack of validation to make sure
    info stored is valid, fewer options with which to “query” our stored data
    (since we can only really do it by dictionary keys), and the inability to
    use object references within a JSON file, resulting in more post-processing
    being necessary.
    2. *SQL/Relational Database*. Pros include a set schema with validation
    whenever inserting new data and support for querying the data based on
    multiple fields (e.g. page number OR title). Cons include needing the SQL
    language to use the database, potentially slow speed, dependence on a
    database instance, and needing to set up an entire database during the
    automation.
    3. *MongoDB, a NoSQL Database*. Pros include flexibility with schemas,
    support for querying using multiple fields, and product-specific
    documentation. Cons include needing to learn the ways for interacting with
    a MongoDB instance and the need to set up an instance during the
    automation.
    4. *.txt files*. Pros include flexibility to store and read data however we
    want and potentially higher I/O speed. Cons include lack of any predefined
    schema (increasing the possibility for things to go wrong).
5. **Rationale** – We decided to use JSON to store our data as it has a much
lower learning curve compared to the database options; does not require us to
set up or maintain a database instance every time we run the code; makes it
much easier to share extracted data between teammates if needed, as compared to
needing to share a database instance; has enough flexibility to store the
relatively simple data structures we are extracting from the old site; can
still be validated with unit tests and checked against a schema; is much more
easily integrated between parts of our code; and still allows the data to be
modified on later passes if necessary (e.g. changing old hyperlinks). Simply
put, we need to create a new data store each time we run the code, and all the
code is meant to run locally on one machine, so we do not need the ACID
properties or transaction management of SQL databases, nor do we need the
scalability of MongoDB. .txt files are not used because they have too little
structure and would require us to check too many things in the code.


## Creating a Static Site, not a Dynamic Web App
1. **Summary** – In order to make the updated version of Excavating Occaneechi
Town into a complete and functioning website, we decided to make it a static
website—the compilation of a number of pages that are displayed essentially
unchanged from how they are stored by the host.
2. **Problem** – This problem comes in the form of question: what format do we
use—on the file level—for the site itself? This problem is significant because
the different potential answers to this question reflect fundamentally
different target formats for our site; therefore, this problem must be solved
before the process of actually creating the new site can begin.
3. **Constraints** – One constraint that we don’t have to worry about here is
extensibility; Excavating Occaneechi Town is ‘complete,’ and no new content
will be published to the site in the future. Our clients have concerns for the
website regarding longevity and the ease of future maintenance, both of which
are important factors for this decision. Cost is also a factor to consider
here; a static solution is almost certainly going to be less expensive than
hosting a webapp, especially considering that the updated site is probably
going to be promoted by UNC Press and might consequently see some traffic. 
4. **Options** –
    1. *Static site, served as files by a web server*. Pros include fast
    loading, low relative complexity, reduced vulnerability to security issues,
    low relative hosting costs, and fewer external dependencies (and therefore
    greater potential longevity). Main con is the reduced capacity for dynamic
    site functionality—one relevant example for us is displaying relational
    data. Some of our site’s data is in the form of related tables; the ability
    to query these tables and perform joins would be very helpful for display,
    but this is basically impossible for a purely static site.
    2. *Standard frontend/backend architecture, with a backend server and a
    database*. Main pro is the ability to use a database for dynamic data
    displays (as described in the example above). Main cons include higher
    design and maintenance complexity, longer response times, potential to
    introduce security vulnerabilities, and dependence on external
    applications and database frameworks for continued functionality.
    3. *Cloud hosting, e.g. with AWS or Firebase*. Pros include many, many
    features for the backend of the app. Cons include cost (such as potentially
    very high costs with Firebase if we do not optimize queries properly) and a
    learning curve.
5. **Rationale** – We settled on a static site implementation for a variety of
reasons. One significant reason is the design complexity of adapting the
currently existing static site to a web app; it will be much simpler for us to
design a static site for our updated version, as most pages of the new site can
correspond one-to-one to pages on the old site. Our clients were also not
particularly concerned with the addition of the sorts of new features that a
database-driven web app would provide; they are mainly looking for an upgrade
to the existing site that will still be dependable and easy to maintain. A
static site will likely provide increased longevity and will be easier to
maintain, as it will have fewer dependencies to potentially break
functionality, and fewer moving parts to break (no backend). The website may
ultimately lack some of the bells and whistles of a fully featured web app, but
it will be fast, functional, and robust as a static site.


## Using Bootstrap, but not a JavaScript Framework
1. **Summary** – In order to give the new website a responsive, mobile-friendly
style with modern features like collapsible and pop-up elements, we decided to
use Bootstrap.
2. **Problem** – Our clients’ primary motivation in seeking an update for their
website is the desire for a design that is mobile-friendly and intuitive. The
current site is implemented with html framesets and no real styling, which
makes using the site on mobile laborsome. Technologies like CSS (and CSS
flexbox) are ubiquitous in modern web design; it is obvious that we will need
to work with stylesheets to make our site responsive to browser size. There is
also the question of adding functionality to the site that was not feasible
when the original site was designed; for example, we can include collapsible
elements like navigation menus that will further improve the mobile experience.
The problem here is not so much about deciding whether or not to do these
things, but rather deciding on what resources to use in doing them.
3. **Constraints** – As mentioned before, our clients are very concerned with
site longevity; the old version of the site has remained almost entirely
functional since it was created in 2003 with very little maintenance. They
would like for the new version of the site to be similarly robust. This entire
problem is a consequence of the obvious and practically universal web design
constraint that a site should look good and be usable on virtually any device.
4. **Options** –
    1. *Fully homemade CSS and JS*. Pros include a clean slate and ultimate
    freedom of design and lack of external dependencies. Cons include the
    increased time and complexity commitments of doing everything from
    scratch, and lack of support.
    2. *Bootstrap*. Pros include a large assortment of components that can
    easily be used for displaying content, an assortment of stylesheets that
    will require little-to-no tweaking to achieve a clean style, and the
    increased likelihood of future support based on its massive popularity.
    Main tradeoff is the introduction of dependency on an external library, and
    the learning curve this introduces (however gentle). 
    3. *Bulma*. Pros are essentially the same as Bootstrap, just with somewhat
    less popularity. One additional pro over Bootstrap is Bulma’s vertical menu
    component, something that Bootstrap lacks out of the box.
    4. *React, Angular, Vue, or other frameworks*. Pros include allowing us to
    have some of the best of both worlds of the static site and web app;
    libraries like React allow for components to be selectively rendered within
    a single page, allowing for more dynamic page features than Bootstrap or
    Bulma alone, all without introducing the need for web app hosting. The
    primary cons are increased complexity, an additional dependency, and an
    additional learning curve to overcome.
5. **Rationale** – We decided on using Bootstrap’s CSS and JS libraries for our
new site design, and no additional JS frameworks. Our main reasoning was
Bootstrap’s low learning curve and popularity, and the desire to keep our
number of dependencies low in the interest of longevity. We are electing not to
use a framework like React.js, as we don’t really have a need for the sorts of
complex functionality that it would provide. We decided on Bootstrap over
alternatives like Bulma mainly because of its popularity; although popularity
is not a guarantee of future support, it is a good predictor for it.
Additionally, the use of Bootstrap will make it more likely that someone tasked
with maintaining the site in the future will be able to understand the
Bootstrap components relatively easily, due to its present ubiquity.


## Using Netlify to Host
1. **Summary** – In order to provide a demo (or complete) version of the site
for debugging and demoing to clients as we work on the project, we decided to
host the site using Netlify.
2. **Problem** – We need to host a working version of the site as part of the
walking skeleton assignment and so our clients can see our work, and also to
perform debugging on the site in case any parts of the extraction or site
generation code have issues. Otherwise, we would have to host sites locally
using something like Node.js, which would not fulfill the walking skeleton
assignment’s requirements.
3. **Constraints** – We want free whenever possible (especially since we have
several options listed below that are free). We also want it to be very easy to
change the files that are hosted in order to fix bugs, or to update the site
with the results of different iterations of our code, meaning the option we
choose should quickly reflect changes and support potentially hundreds of
changes constantly occurring in a span of two months (from October to end of
semester). Additionally, since our finished product should be a static site, we
do not need our choice for hosting to support a backend server or databases.
4. **Options** –
    1. *Netlify*, an “all-in-one platform for automating modern web projects”.
    Pros include a feature-loaded free tier, support specifically for static
    sites, support for CI/CD and integration with GitHub (to the point that a
    single push can update the site), support for setting up a unc.edu domain
    name to redirect to Netlify, and the ability to ask Dr. Terrell for help
    during office hours due to his usage of Netlify. Cons include potential
    limits on the free plan and needing to transfer ownership of the site to
    the clients on our own.
    2. *UNC Library/iBiblio Hosting*, which is possible depending on their
    cooperation. Pros include “official-ness” of our project and potentially
    higher visibility to people who haven’t visited the site before. Cons
    include difficulties modifying the files once we hand them over to be
    hosted.
    3. *OASIS hosting*, provided by the UNC Office of Arts and Sciences
    Information Services. Pros include past usage for the Fall 2018 Electronic
    Dig remake and even for the current Excavating Occaneechi Town website, low
    or no cost, and familiarity with OASIS through the client or through one of
    the team members. Cons include needing to go through extra steps to modify
    the files as compared to an option like Netlify or Heroku.
    4. *Heroku*. Pros include a great free tier, great popularity and
    documentation, and support for dynamic web app features should we need
    them. Cons include potentially less help from office hours compared to
    Netlify and potential free tier limitations.
5. **Rationale** – We chose Netlify after consulting with Dr. Terrell as it’s
very well suited to hosting static sites (which our new site will be). The free
tier should support everything we need, and CI/CD features and integration with
GitHub allow us to easily iterate and are a huge plus. We can still use Heroku
if needed since it’s all free (except for the learning curve), and once we
finish the project and iron out the bugs, we can still host the finished
product through OASIS if needed or the UNC Library if they would like us to.
