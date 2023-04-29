from transformers import AutoTokenizer, T5ForConditionalGeneration
tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-large")
model = T5ForConditionalGeneration.from_pretrained("Salesforce/codet5-large")

text='''
function CardGroup(props) {  
  const {
    centered,
    children,
    className,
    content,
    doubling,
    items,
    itemsPerRow,
    stackable,
    textAlign,
  } = props
  const classes = cx(
    'ui',
    useKeyOnly(centered, 'centered'),
    useKeyOnly(doubling, 'doubling'),
    useKeyOnly(stackable, 'stackable'),
    useTextAlignProp(textAlign),
    useWidthProp(itemsPerRow),
    'cards',
    className,
  )
  const rest = getUnhandledProps(CardGroup, props)
  const ElementType = getElementType(CardGroup, props)
  if (!childrenUtils.isNil(children)) {
    return (
      <ElementType {...rest} className={classes}>
        {children}
      </ElementType>
    )
  }
  if (!childrenUtils.isNil(content)) {
    return (
      <ElementType {...rest} className={classes}>
        {content}
      </ElementType>
    )
  }
  const itemsJSX = _.map(items, (item) => {
    const key = item.key || [item.header, item.description].join('-')
    return <Card key={key} {...item} />
  })
  return (
    <ElementType {...rest} className={classes}>
      {itemsJSX}
    </ElementType>
  )
}
/* is used to<extra_id_0>
'''
#Returns a dictionary from a URL params
text=text.replace('\n','\r\n')
print(text+'\n\n')
input_ids = tokenizer(text, return_tensors="pt").input_ids

# simply generate a single sequence
generated_ids = model.generate(input_ids, max_length=25)
print(tokenizer.decode(generated_ids[0], skip_special_tokens=False))
