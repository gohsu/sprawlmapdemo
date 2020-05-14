import plots
import get_data
import create_desc

# this is just a test
mode = "incremental"

f = open("ontario.html", "a+")
front_matter = """
<head>
    <html lang="en"></html>
    <meta charset="utf-8"/>
    <title>SNDI</title>
    <style>
        body{
            max-width: 800px;
            font-family:sans-serif;
            text-align: center;
            margin:auto;
        }

        h2,p{
            padding-top: 1em;
            text-align: justify;
        }

        h3{
            text-decoration: underline;
        }

        div{
            margin:auto;
        }

        .dropbtn {
            font-size: larger;
            cursor: pointer;
            background-color: transparent;
            text-decoration: underline;
            border:none;
        }

        /* The container <div> - needed to position the dropdown content */
        .dropdown {
            font-size: large;
            position: relative;
            display: inline-block;
        }

        /* Dropdown Content (Hidden by Default) */
        .dropdown-content {
            display: none;
            position: absolute;
            background-color:white;
            box-shadow: 0px 5px 10px 0px rgba(0,0,0,0.2);
            z-index: 1;
            white-space: nowrap;
        }

        /* Links inside the dropdown */
        .dropdown-content a {
            padding: 10px 20px;
            display: block;
            font-size: medium;
            text-decoration: none;
        }

        /* Change color of dropdown links on hover */
        .dropdown-content a:hover {background-color: #f1f1f1}

        /* Show the dropdown menu on hover */
        .dropdown:hover .dropdown-content {
            display: block;
        }

    </style>    

</head>
"""
dropdown = """
 <h2>
        Canada :
        <div class="dropdown">
            <button class="dropbtn">Provinces</button>
            <div class="dropdown-content">
                <a href="#">British Columbia</a>
                <a href="#">Alberta</a>
                <a href="#">Saskatchewan</a>
                <a href="#">Manitoba</a>
                <a href="#">Ontario</a>
                <a href="#quebec">Quebec</a>
                <a href="#">New Brunswick</a>
                <a href="#">Nova Scotia</a>
                <a href="#">Newfoundland and Labrador</a>
        </div>
    </h2>"""
f.write(front_matter)
f.write(dropdown)

region_filename = "Ontario".casefold()
plots.plot_regional("Ontario",mode).savefig("on-plots/{}.png".format(region_filename))

quebec = """
    <div>
        <h2><a name="quebec"><a href="">Canada</a>: Quebec</a></h2>
        <img src='qc-plots/{}.png'>
    </div>
        """.format(region_filename)

ontario = """
    <div>
        <h2><a name="ontario"><a href="">Canada</a>: Ontario</a></h2>
        <img src='on-plots/{}.png'>
    </div>
        """.format(region_filename)

# f.write(quebec)
f.write(ontario)

quebec_cities = get_data.get_region_cities_list("Québec")
ontario_cities = get_data.get_region_cities_list("Ontario")

for city in ontario_cities:
    city_filename = city.replace(" ","").casefold()
    plots.plot_city(city,mode).savefig("on-plots/{}.png".format(city_filename))
    city_desc = create_desc.city_desc(city)
    ranking_desc = create_desc.ranking_desc(city)
    f.write("<div>")
    f.write("<h2>Ontario : {}</a></h2>".format(city))
    f.write("<img src='on-plots/" + city_filename + ".png' />")
    f.write("<p>" + city_desc + "</p>")
    f.write("<p>" + ranking_desc + "</p>")
    f.write("</div>")

f.write("</body>")
f.write("</html>")
f.close()
