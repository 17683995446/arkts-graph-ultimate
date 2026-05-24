
/**
 * 极度混乱的文件5 - 极端格式
 */
@Component export struct NoSpaceClass { private a:number=0; private b:string=""; method():void{console.log('无空格');} build(){Column(){}}}
@Component export struct OneLineClass{private count:number=0;inc():void{this.count++;}dec():void{this.count--;}build(){Row(){}}}
@Component export struct NormalClass{private value:number=42;get():number{return this.value;}set(v:number):void{this.value=v;}build(){Stack(){}}}
