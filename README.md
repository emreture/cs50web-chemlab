# Project Final [![Build Status](https://travis-ci.com/emreture/cs50web-chemlab.svg?branch=master)](https://travis-ci.com/emreture/cs50web-chemlab)

Web Programming with Python and JavaScript

## Django web application for a chemistry laboratory

In this project, I've built a web application for handling sample records and analysis results of a chemistry laboratory that performs gasoline and gas oil analysis.

Using this web application,
- Laboratory staff can add/edit samples, enter analysis results of samples and add/edit customers of the laboratory.
- Laboratory managers can also add/edit test methods and products to be analyzed.
- Customers of the laboratory can see analysis results of their samples.

Laboratory customers are legal entities. Laboratory managers can associate website users with customers using the site administration page.

## Models

Django’s built-in authentication and user model is used for logging users in and out.

Customers of the laboratory is modelled in ```Customer``` class. This class has name (company name), address and users fields. Users is a many to many field to Django's user model.

Test methods used for analysis of samples are modelled in ```TestMethod``` class which has number, name and unit properties.

Products are modelled in ```Product``` class. It has a name and a tests field which is a many to many field to ```TestMethod``` class. Some tests are applied to certain products.

Sample details are modelled in ```Sample``` class. Its fields are number, receipt date, product (foreign key to ```Product```), customer (foreign key to ```Customer```), sampling date, sampling point and report date.

First of all, users should be created by laboratory managers using Django's built in admin app. Superuser status should be active for laboratory managers and staff status should be active for laboratory staff. Customer users are associated with customers when customers are created. Only laboratory managers can create users.

Customers are created in the admin app. When adding/editing a customer object, users of that customer can be selected. Laboratory staff can add and edit customers using website's customers page. Only laboratory managers can delete customers and associate users with customers using the admin app. Customers also can be added and edited by laboratory staff using customers app. Link to customers app is located on the navbar. But laboratory staff can not associate users with customers.

After creating users and customers, test methods that will be performed in the laboratory should be defined. Then products and test methods to be applied to these products should be determined. Both test methods and products are added, edited and deleted using the admin app by laboratory managers.

Chemlab web application is ready to go after creating objects mentioned above.

Laboratory staff can add and edit samples received by using the samples app. Links to 'List samples' and 'Add sample' are located on the navbar. Sample numbers are assigned automatically and can not be edited. Only laboratory managers can delete samples and change sample numbers using the admin app.

Analysis results of samples can be entered using the results app by laboratory staff. Link to 'Analysis results' is located on the navbar

## Web pages
### Navigation bar
Customers can only see 'Home' and 'Analysis results' links on the navbar. In addition to these links laboratory staff can see 'Samples' (list samples and add sample) and 'Customers' link. Laboratory manager can see all of the links including the 'Site administration' link on the navbar.

### Homepage (/)
This is the landing page of the website. A brief introduction about this website is presented on this page.

### Log in (/accounts/login) page
If a user is not authenticated, a link for log in is shown on the navigation bar. Users (customer users, laboratory staff and laboratory managers) can log in using the form on the log in page.

### Log out (/accounts/logout) page
When a user is authenticated, a log out link is shown on the navigation bar instead of log in link. When an authenticated user clicks on that link, he/she is logged out.

### Viewing samples (/samples and /samples/<int:sample_id>)
Laboratory staff can see a list of samples received on this page. When a user click on a sample listed, he/she is directed to a page where he/she can edit details of the sample.

### Adding new samples (/samples/add)
New samples can be added using 'Add sample' page. Laboratory staff can access to this page by simply clicking on the 'Add sample' link under the 'Samples' dropdown list on the navbar.

Users can press the 'Add' button after filling the form to add a new sample or can press the 'Cancel' button to go back to the sample list page.

### Viewing and editing analysis results (/results and results/<int:sample_id>)
On the 'analysis results' page, laboratory staff can see a list of all samples received, while customer users can only see samples from their company.

When a user click on the sample, he/she is directed to a page where he/she can see analysis results of that sample. Laboratory staff can edit results on this page.

### Customers page (/customers)
Laboratory staff can see a list of registered customers and add a new customer using the form below the list on this page.

When a customer is clicked, user is directed to a page where he/she can edit its details. Users can not be associated with customers on this page. This action can be done by only laboratory managers using the admin app.

## Finally
I'd like to thank all the people who made this great [CS50's Web Programming with Python and JavaScript course](https://www.edx.org/course/cs50s-web-programming-with-python-and-javascript) possible and also thank you to [Brian Yu](https://www.edx.org/bio/brian-yu) for his fluency and easy-to-understand lectures.
