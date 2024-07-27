import os
import logging
from lxml import etree

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARN').upper()
logging.basicConfig(level=LOGLEVEL)
logger = (logging.getLogger(__name__),)

XSLT_TRANSFORM = etree.XSLT(
    etree.XML(
        """<?xml version="1.0"?>
        <xsl:stylesheet version="1.0"
        	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >
        	<xsl:template match="/">
        		<xsl:for-each select="multivalue/tuple">
        			<Detail>
        				<Amount>
        					<xsl:value-of select="datapoint[@schema_id='item_amount_total'] " />
        				</Amount>
        				<Quantity>
        					<xsl:value-of select="datapoint[@schema_id='item_quantity'] " />
        				</Quantity>
        			</Detail>
        		</xsl:for-each>
        	</xsl:template>
        </xsl:stylesheet>"""
    )
)

MAPPING_DICT = {"item_quantity": "Quantity", "item_amount_total": "Amount"}

# def prettyprint(element, **kwargs):
#     xml = etree.tostring(element, pretty_print=True, **kwargs)
#     print(xml.decode(), end='')

# My first thought was to use Pandas/Polars or similar but later I realised it is not a shallow XML (I mean to use it for the <Details/> part and there are repeated elements).
# After writing piece of code I was thinking about XSLT, XQuery, iter or just converting to dict (mapping schema_id to keys) and then just assigning values.
# In real case I would sit down and do some execution time and memory consumption comparisons.
# For simplification I do not copy all attributes.


def transform(input: str) -> dict:

    logging.debug("Got input data %s", input)

    root = etree.fromstring(input)
    content = root.xpath('//export/results/annotation//content')[0]

    output = etree.Element('InvoiceRegisters')
    payable = etree.SubElement(etree.SubElement(output, 'Invoices'), 'Payable')

    # for "header" values I could use xpath
    info = content.xpath('./section[@schema_id="invoice_info_section"]')[0]
    invoice_no = info.xpath('./datapoint[@schema_id="invoice_id"]/text()')[0]
    logging.debug("Parsing invoice no %s", invoice_no)
    etree.SubElement(payable, 'InvoiceNumber').text = invoice_no

    amounts = content.xpath('./section[@schema_id="amounts_section"]')[0]
    etree.SubElement(payable, 'TotalAmount').text = amounts.xpath('./datapoint[@schema_id="amount_total"]/text()')[0]
    # etc ...

    # Here I could use iter, XSLT, conversion to dict, most probably not XQuery and not Pandas/Polars. The right selection is based on:
    # - proper transformation description
    # - speed and memory requirements
    # - code readability and maintainability
    # - team libs knowledge
    # - I migth create some framework if we use it in more places

    line_items = content.xpath('./section[@schema_id="line_items_section"]/multivalue')[0]

    # XSLT way:
    # etree.SubElement(payable, 'Details').append(XSLT_TRANSFORM(line_items).getroot())

    # iter way:
    details = etree.SubElement(payable, 'Details')
    for line in line_items.iter("tuple"):
        detail = etree.SubElement(details, 'Detail')  # can cause empty <Detail/> element
        for datapoint in line.iter("datapoint"):
            element = MAPPING_DICT.get(datapoint.get("schema_id"))
            if element:
                etree.SubElement(detail, element).text = datapoint.text

    # TODO if log level is debug then:
    logging.debug("Output data %s", etree.tostring(output).decode())

    return etree.tostring(output)
